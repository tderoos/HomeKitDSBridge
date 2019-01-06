# from http.client import HTTPSConnection
# from base64 import b64encode
# import ssl

# This sets up the https connection
# c = HTTPSConnection("digitalstrom.local", context=ssl._create_unverified_context())
# we need to base 64 encode it
# and then decode it to ASCII as python 3 stores it as a byte string
# userAndPass = b64encode(b"username:password").decode("ascii")
# headers = {'Authorization': 'Basic %s' % userAndPass}
# then connect
# c.request('GET', '/', headers=headers)
# get the response back
# res = c.getresponse()
# at this point you could check the status etc
# this gets the page text
# data = res.read()

# print(data)
# 5f129b3e67c3112968cab121b036289c929509b6b5527b0dcc0b92476199812d


# b'{"result":{"applicationToken":"2480ec583abca051318701c17f08989b48773c13f61115dfd1e88123b0d6f631"},"ok":true}'
import requests
import json
from requests.auth import HTTPBasicAuth
import PySimpleGUI as sg

import DigitalStrom

#ds = DigitalStrom(u"https://digitalstrom.local:8080/")

server = u"https://digitalstrom.local:8080/"
action_getname = u"json/apartment/getName"
action_login = u"json/system/loginApplication?loginToken=2480ec583abca051318701c17f08989b48773c13f61115dfd1e88123b0d6f631"
passwd = u"&username=dssadmin&password={6Z93MnwDA9Zoyz^"
apptoken = u"&token=2480ec583abca051318701c17f08989b48773c13f61115dfd1e88123b0d6f631"
# url = u"https://digitalstrom.local"

# url = u"https://digitalstrom.local/json/device/setValue?_dc=1544125657384&dsuid=303505d7f80000000000004000040b7600&value=13&category=manual"

url = server + action_login

# url = u"https://digitalstrom.local:8080/json/system/requestApplicationToken?applicationName=dss2homekit"

# auth = HTTPBasicAuth('dssadmin', '{6Z93MnwDA9Zoyz^')


# r = requests.get(url=url, auth=auth, verify=False)

r = requests.get(url=url, verify=False)

response = json.loads(r.content)
sessiontoken = u"&token=" + response["result"]["token"]

r = requests.get(server + "json/apartment/getStructure" + sessiontoken, verify=False)
structure = json.loads(r.text)
url = server + "json/device/blink?dsid=303505d7f80000000000004000040b76" + sessiontoken
#r = requests.get(server + "json/device/blink?dsuid=303505d7f80000000000004000040b7600" + sessiontoken, verify=False)
#print(r.content)


tab1_layout =  [[sg.T('This is inside tab 1')]]

tab2_layout = [[sg.T('This is inside tab 2')],
               [sg.In(key='in')]]

layout = [[sg.TabGroup([[sg.Tab('Tab 1', tab1_layout, tooltip='tip'), sg.Tab('Tab 2', tab2_layout)]], tooltip='TIP2')],
          [sg.Button('Read')]]

window = sg.Window('My window with tabs', default_element_size=(12,1)).Layout(layout)

while True:
    event, values = window.Read()
    print(event,values)
    if event is None:           # always,  always give a way out!
        break