import requests
import json
import sys
from time import sleep
import credentials
import servername
import pprint
import csv

server = 'ns-us-dcc.sensity.com'
manserver ='man-leg.sensity.com'

def GetNodes():
# This will get a list of all nodes on a server and provide the URL to make changes in Site, Node, URL format

    session = requests.session()
    headers = {'content-type': 'application/json',
               'api_key': credentials.api_key_mfg}
    print(servername.servername)

    url = session.get(url='https://' + servername.servername + '/v3.0/customers/', headers=headers, verify=False)

    print(json.loads(url.text)[0]['name'])
    mfgorgid = json.loads(url.text)[0]['orgid']

    sitelist = session.get(url='https://' + servername.servername + '/v3.0/customers/' + mfgorgid + '/sites',
                           headers=headers)
    print(sitelist)
    responsedict = {}

    for i in json.loads(sitelist.text):
        responsedict[i['name']] = i['siteid']
    # pprint.pprint(responsedict)
    nodedict = {}
    nodelist = []
    for key, val in responsedict.items():

        nodes = session.get(url='https://' + servername.servername + '/v3.0/customers/' + mfgorgid + '/sites/'
                                + val + '/nodes')
        url = 'https://' + servername.servername + '/v3.0/customers/' + mfgorgid + '/sites/' + val + '/nodes/redirect'
        for i in json.loads(nodes.text):
            nodedict.update({i['nodeid'] : [key , url]})

    return nodedict


def NodeSearch(filename):
    #this function will intake results from GetNodes() and only output the items that exist the file provided
    filtered_dict = {k:v for (k, v) in GetNodes().items() if k in ReadFile(filename)}
    return filtered_dict

def PushJsonToServer(node,nsserver,ns_url):
    headers = {'content-type': 'application/json',
               'api_key': credentials.api_key_mfg}
    pushpacket = requests.session()
    payload ={}
    payload["nodeList"] = [node]
    payload["server"] = nsserver
    print(ns_url)
    print(payload)
    pushpacket.post(ns_url, headers=headers, data=json.dumps(payload))


def NodeDeploy(filename):
    for k,v in NodeSearch(filename).items():
        response = PushJsonToServer(k,server,v[1])
        print(response)


def ReadFile(filename):
    #This function reads the contents of csv and extracts all nodes
    item_list = []
    with open(filename, 'rt') as f:
        item_list.extend(i[0] for i in csv.reader(f))
    return item_list

#PushJsonToServer('N0123456','me.com', 'https://1.2.3.4/')

NodeDeploy('test2.csv')

#print(ReadFile('test2.csv'))

