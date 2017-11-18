import requests
import json
import csv
import credentials
import servername


def DeleteNode(filename, orgid, siteid):
    session = requests.session()
    headers = {'content-type': 'application/json',
               'api_key': credentials.api_key_ns}

    for i in ReadFile(filename):
        response = session.post(url='https://' + servername.nsservername + '/v3.0/customers/' + orgid + '/sites/'
                        + siteid + '/nodes/deactivate/' + i , headers=headers )
        print(json.dumps(response.text))
        print(response)



def ReadFile(filename):
    #This function reads the contents of csv and extracts all nodes
    item_list = []
    with open(filename, 'rt') as f:
        item_list.extend(i[0] for i in csv.reader(f))
    print(item_list)
    return item_list


DeleteNode('test3.csv','13ee6f0-927e-11e7-b9e8-696802539e21','4bd84a10-927e-11e7-b9e8-696802539e21')