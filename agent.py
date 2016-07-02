#!virtenv/bin/python
## This provides a wrapper for check_mk_agent and sends it's output to an API collector

import requests, json, socket, os, subprocess, argparse
from random import randint
from time import sleep
from base64 import b64encode
from urllib import urlencode

api_base_url = 'http://127.0.0.1:8080/collector/api/v0.1/hosts/'
hostname = socket.gethostname()

## If CMK Agent script doesn't exist then exit
if not os.path.isfile('/usr/bin/check_mk_agent'):
    print "ERR: can't find /usr/bin/check_mk_agent"
    exit(1)

def main():
    ## Parse CommandLine arguments
    ## https://docs.python.org/2/howto/argparse.html
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--daemonize", action="store_true", help="Run in background")
    parser.add_argument("-v", "--verbose", action="store_true", help="Run verbosely")
    args = parser.parse_args()
    
    ## If daemonize=True, run in loop
    if args.daemonize:
        while True:
            send_status(get_status())
            sleep(15 + randint(-3,3))
    ## Otherwise, run once and exit
    else:
        send_status(get_status())

    exit(0)
    

def get_status():
    data = {}
  
    ## Open subprocess to get check_mk_agent output)
    p = subprocess.Popen('/usr/bin/check_mk_agent', stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    
    ## Base64 encode the check_mk_agent output so we can cleanly pass it over the API
    status_data = b64encode(output)
  
    data['hostname'] = hostname
    data['status_data'] = status_data
    
    return data


def send_status(data):
    r = requests.put(api_base_url + hostname, json=data)
    print r.headers
        
    
if __name__ == '__main__':
    main()