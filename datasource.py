#!virtenv/bin/python
## Connects to API to retrieve status data for hosts

import argparse, requests
import json
from base64 import b64decode

def main():
    ## Parse CommandLine arguments
    ## https://docs.python.org/2/howto/argparse.html

    parser = argparse.ArgumentParser()
    parser.add_argument("--host", "--hostname", required=True, help="Hostname to get status data for")
    parser.add_argument("--api", "--api_base_url", required=False, help="API Base URL", default='http://127.0.0.1:8080/collector/api/v0.1/hosts')

    args = parser.parse_args()
    hostname = args.host
    api_base_url = args.api

    get_status(hostname,api_base_url)


def get_status(hostname,api_base_url):
    r = requests.get(api_base_url + '/' + hostname)
    if r.status_code == 404:
        add_new_host(hostname,api_base_url)
    elif r.status_code != 200:
        print("Error getting status")
        exit(1)
    else:
        j = json.loads(r.content)
        data = j['host']
        print_status(data)


def print_status(data):
    if data['status_data']:
        ## Check that the status_data was generated within the last 120 seconds
        if data['status_age'] < 120:
            status_data = b64decode(data['status_data'])
            print status_data
            exit(0)
        else:
            print "status_data is out of date :("
            exit(1)
    else:
        exit(1)


def add_new_host(hostname,api_base_url):
    ## If CMK requests a host that doesn't exist, we create a new host entry on the API
    data = {}
    data['hostname'] = hostname
    data['status_data'] = None

    ## POST new host to API
    r = requests.post(api_base_url, json=data)
    print r.json()

    if r.status_code == 200:
        exit(0)
    else:
        exit(1)


if __name__ == '__main__':
    main()
