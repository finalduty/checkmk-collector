#!/bin/bash

api_base_url='http://127.0.0.1/collector/api/v0.1/status'
data=`/usr/bin/check_mk_agent | base64 -w0 | head -c30`
host_name=`hostname -f`
status_code=`curl -I $api_base_url/$host_name 2>/dev/null | awk '/HTTP/ {print $2}'`

if [ $status_code -eq 200 ]; then
	method=PUT
	uri="$api_base_url/$host_name"
elif [ $status_code -eq 404 ]; then
	method=POST
	uri=$api_base_url
fi

curl -i -H "Content-Type: application/json" -X $method -d '{"hostname":"'`echo $host_name`'","status_data":"'`echo $data`'"}' $uri