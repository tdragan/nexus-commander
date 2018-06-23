#!/usr/bin/env python3
import requests
from requests.auth import HTTPBasicAuth
import argparse
from operator import itemgetter


# store arguments in a file
# kad se lista image napisati broj instanci
# keep last n images
# error catching
# fix host, port vars to be prettier
# remove proxy if exists in env

def query_repo():
    host = args.host
    port = args.port
    repo = args.repository
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


def delete_image(name, tag):
    host = args.host
    port = args.port
    username= args.username
    password= args.password
    json_data = query_repo()
    toRemove = get_id(name, tag)
    print("Deleting image(s): " + name + ":" + tag + "          with ID(s):", toRemove)
    d = requests.delete("http://" + host + ":" + port + "/service/rest/beta/components/" + toRemove + "",
                        auth=HTTPBasicAuth(username, password))


def list_all_repos():
    host = args.host
    port = args.port
    print("List of all Nexus repositories:")
    r = requests.get("http://" + host + ":" + port + '/service/rest/beta/repositories')
    repo_data = r.json()
    for value in repo_data:
        print(value['name'])


def list_images_by_name(name):
    print("List of all images by name: " + name)
    lista = query_repo()
    for value in lista:
        if value['name'] == name:
            print(value['name'] + ':' + value['version'])


def list_images_by_tag(tag):
    print("List of all images by tag: " + tag)
    lista = query_repo()
    for value in lista:
        if value['version'] == tag:
            print(value['name'] + ':' + value['version'])


def delete_images_by_name(name):
    print("Error: Option disabled")
    #print("Deleting images by name: " + name)
    #json_data = query_repo()
    #for value in json_data['items']:
    #    tag = value['version']
    #    if value['name'] == name:
    #        delete_image(name, tag)


def delete_images_by_tag(tag):
    print("Deleting images by tag: " + tag)
    lista = query_repo()
    for value in lista:
        name = value['name']
        if value['version'] == tag:
            delete_image(name, tag)


parser = argparse.ArgumentParser()
parser.add_argument("action", help=":specify an action", choices=["list", "delete", "repos"])
parser.add_argument("-n", "--name", help="specify image name. Used in list and delete commands")
parser.add_argument("-t", "--tag", help="specify image tag. Used in list and delete commands")
parser.add_argument("--host", help="specify target Nexus hostname. Default is localhost", default="localhost")
parser.add_argument("--port", help="specify target Nexus port. This is web access port. Default is 8081", default="8081")
parser.add_argument("-u", "--username", help="specify Nexus login username. Default is admin", default="admin")
parser.add_argument("-p", "--password", help="specify Nexus login password. Default is admin123", default="admin123")
parser.add_argument("--repository", help="specify target Nexus docker repository. Default is docker_repo", default='docker_repo')

args = parser.parse_args()

if args.action == "list" and args.name is not None and args.tag is None:
    list_images_by_name(args.name)
elif args.action == "list" and args.tag is not None and args.name is None:
    list_images_by_tag(args.tag)
elif args.action == "list" and args.name is None and args.tag is None:
    list_all_images()
    #sort_images()

if args.action == "repos":
    list_all_repos()

if args.action == "delete" and args.name is not None and args.tag is None:
    delete_images_by_name(args.name)
elif args.action == "delete" and args.name is None and args.tag is not None:
    delete_images_by_tag(args.tag)
elif args.action == "delete" and args.name is not None and args.tag is not None:
    delete_image(args.name, args.tag)
elif args.action == "delete" and args.name is None and args.tag is None:
    print("Error: Delete command requires an argument. Please state image name(-n) or tag(-t) or both")

