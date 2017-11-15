import credentials
import servername
import pprint

import requests
import json

server = 'ns-us-dcc.sensity.com'
man-server='man-leg.sensity.com'

def results():
    # specify the url
    session = requests.session()
    headers = {'content-type': 'application/json',
               'api_key': '807d8cf3c97d4559de71686c7e57684d90d753ec'}
    print(servername.servername)

    url = session.get(url='https://' + servername.servername + '/v3.0/customers/', headers=headers , verify=False)

    print(json.loads(url.text)[0]['name'])
    mfgorgid = json.loads(url.text)[0]['orgid']

    sitelist = session.get(url='https://' + servername.servername + '/v3.0/customers/' + mfgorgid + '/sites' , headers=headers )

    responsedict = {}

    for i in json.loads(sitelist.text):
        responsedict[i['name']] = i['siteid']
    #pprint.pprint(responsedict)
    nodedict = {}
    nodelist = []
    for key, val in responsedict.items():

        nodes = session.get(url='https://' + servername.servername + '/v3.0/customers/' + mfgorgid + '/sites/'
                                + val + '/nodes' )
        url ='https://' + servername.servername + '/v3.0/customers/' + mfgorgid + '/sites/' + val + '/nodes'
        for i in json.loads(nodes.text):
            nodelist.append(key + ':' + i['nodeid'] + ',' + url + '/' + i['nodeid'])
    return nodelist


pprint.pprint(results())