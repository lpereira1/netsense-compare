import csv
import json
import pprint
import requests
import credentials
import servername

server = 'ns-us-dcc.sensity.com'
manserver ='man-leg.sensity.com'


def GetUsers():
# This will get a list of all nodes on a server and provide the URL to make changes in Site, Node, URL format

    session = requests.session()
    headers = {'content-type': 'application/json',
               'api_key': credentials.api_key_zabbed}
    print(servername.servername)

    url = session.get(url='https://' + servername.nsservername + '/v3.0/customers/', headers=headers)

    print(json.loads(url.text)[0]['name'])
    mfgorgid = json.loads(url.text)[0]['orgid']

    customerlist = session.get(url='https://' + servername.nsservername + '/v3.0/customers/' , headers=headers)
    responsedict = {}
    #for debug
    #print(json.loads(customerlist.text))


    for i in json.loads(customerlist.text):
        responsedict[i['name']] = i['orgid']
    #pprint.pprint(responsedict)
    userdict = {}
    for key, val in responsedict.items():
        users = session.get(url='https://' + servername.nsservername + '/v3.0/customers/' + val + '/users/', headers=headers)
        suspended_users= session.get(url='https://' + servername.nsservername + '/v3.0/customers/' + val + '/suspended-users' , headers=headers)
        #for debug
        #print(json.loads(users.text))
        for i in json.loads(users.text):
            #print(key + ' - ' + i['name'] + ' - ' + i['email'] )
            userdict.update({i['email'] : [i['name'], key ]})
        for i in json.loads(suspended_users.text):
            userdict.update({i['email'] : [i['name'], key ]})


    return userdict




pprint.pprint(GetUsers())

