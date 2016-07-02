#!virtenv/bin/python
## Provides API for CMK Collector Service

from flask import Flask, jsonify, abort, make_response, request, url_for
from datetime import datetime

app = Flask(__name__)
base_url = '/collector/api/v0.1'

## Tidy JSON error responses
## 400 Bad Request
@app.errorhandler(400)
def error_400(error):
    return make_response(jsonify({
        'error': 'Bad Request'
    }), 400)

## 404 Not Found    
@app.errorhandler(404)
def error_404(error):
    return make_response(jsonify({
        'error': 'Not Found'
    }), 404)
 
## 405 Method Not Allowed
@app.errorhandler(405)
def error_405(error):
    return make_response(jsonify({
        'error': 'Method Not Allowed'
    }), 405)

## 422 Unprocessable Entity
@app.errorhandler(422)
def error_406(error):
    return make_response(jsonify({
        'error': 'Uprocessable Entity', 
        'info': 'Use PUT instead of POST'
    }), 422)

hosts = [
    {
        'hostname': u'example.host',
        'last_updated': None,
        'status_data': None,
    }
]

## Add full URI to response
def make_public_uri(response):
    new_response = {}
    
    for field in response:
        if field == 'hostname':
            new_response['uri'] = url_for('get_host', hostname = response['hostname'], _external=True)
        new_response[field] = response[field]
    
    return new_response

## GET Functions 
## Future updates will enforce access by slaves or admins only   
@app.route(base_url + '/hosts', methods=['GET'])
def get_hosts():
    return jsonify({'hosts': map(make_public_uri, hosts)})

@app.route(base_url + '/hosts/<hostname>', methods=['GET'])
def get_host(hostname):
    host = [host for host in hosts if host['hostname'] == hostname]
    
    if len(host) == 0:
        abort(404)
    
    return jsonify({'host': make_public_uri(host[0])})
    
    

## PUT Functions (
## Future updates will enforce authenticated access by clients
@app.route(base_url + '/hosts/<hostname>', methods=['PUT'])
def update_host_status(hostname):
    host = [host for host in hosts if host['hostname'] == hostname]

    if len(host) == 0:
        abort(404)
    if not request.json:
        print 'json'
        abort(400)
    if 'hostname' in request.json and type(request.json['hostname']) != unicode:
        print 'hostname'
        abort(400)
    if 'status_data' in request.json and type(request.json['status_data']) != unicode:
        print 'data'
        abort(400)

    host[0]['hostname'] = host[0]['hostname']
    host[0]['last_updated'] = datetime.now()
    host[0]['status_data'] = request.json.get('status_data', host[0]['status_data'])
    
    return jsonify({'host': make_public_uri(host[0])})

    
## POST Functions 
## Future updates will enforce access by slaves or admins only
@app.route(base_url + '/hosts', methods=['POST'])
def add_host():
    print "POST"
    if not request.json or not 'hostname' in request.json:
        abort(400)
    hostname = request.json['hostname']
        
    for host in hosts:
        if host['hostname'] == hostname:
            abort(422)

    host = {
        'hostname': hostname,
        'last_updated': datetime.now(),
        'status_data': request.json.get('status_data', "")
    } 

    hosts.append(host)

    return jsonify({'host': make_public_uri(host)})


## DELETE Functions 
## Future updates will enforce access by slaves or admins only
@app.route(base_url + '/hosts/<hostname>', methods=['DELETE'])
def delete_host(hostname):
    host = [host for host in hosts if host['hostname'] == hostname]
    
    if len(host) == 0:
        abort(404)
    
    if hosts.remove(host[0]):
        return jsonify({'result': True})
    else:
        return jsonify({'result': False})
    

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
