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
        url = 'https://' + servername.servername + '/v3.0/customers/' + mfgorgid + '/sites/' + val + '/redirect'
        for i in json.loads(nodes.text):
            nodedict.update({i['nodeid'] : [key , url]})

    return nodedict


def NodeSearch(filename):
    filtered_dict = {k:v for (k, v) in GetNodes().items() if k in ReadFile(filename)}
    return filtered_dict

def NodeDeploy(filename):
    jsonresponse = { 'server' : server}
    for k,v in NodeSearch(filename).items():

        print(k + ',' + str(jsonresponse))


def ReadFile(filename):
    with open(filename, 'rt') as f:
        item_list = (i[0] for i in csv.reader(f))
    return item_list

NodeDeploy('test.csv')

#print(ReadFile('test.csv'))

