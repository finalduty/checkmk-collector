#!virtenv/bin/python
## Connects to API to retrieve status data for hosts

import argparse, requests
from base64 import b64decode

api_base_url = 'http://127.0.0.1/collector/api/v0.1/hosts/'

def main():
    ## Parse CommandLine arguments
    ## https://docs.python.org/2/howto/argparse.html
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", "--hostname", required=True, help="Hostname to get status data for")
    
    args = parser.parse_args()
    hostname = args.host
    
    get_status(hostname)
    


def get_status(hostname):
    r = requests.get(api_base_url + hostname)
    data = r.json()['host']
    status_data = b64decode(data['status_data'])
    print status_data
    
if __name__ == '__main__':
    main()
    
    