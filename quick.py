#!/usr/bin/env python3
import requests
from requests.auth import HTTPBasicAuth
import argparse

def query_repo():
    # http://localhost:8081/service/rest/beta/components?continuationToken=dfbef09efe1644ea13198eec17826be0&repository=docker_repo
    req = requests.get('http://localhost:8081/service/rest/beta/components?repository=docker_repo')
    json_data = req.json()
    token = json_data['continuationToken']
    sum = []
    while token is not None:
        req_with_token = requests.get('http://localhost:8081/service/rest/beta/components?continuationToken=' + token + '&repository=docker_repo')
        json_data2 = req_with_token.json()
        token = json_data2['continuationToken']
        sum = sum + json_data2['items']
    return sum + json_data['items']

def get_id(name, tag):
    lista = query_repo()
    for value in lista:
        if value['name'] == name and value['version'] == tag:
            print(value['id'])

def list_all_images():
    print("List of all images:")
    lista = query_repo()
    for value in lista:
        print(value['name'] + ':' + value['version'])

# query_repo()
get_id("busybox", "latest")
# list_all_images()
