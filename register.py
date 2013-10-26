import sys
import json
import requests
from requests.auth import HTTPBasicAuth
from uuid import getnode as get_mac

URL_ROOT = 'http://autopi.herokuapp.com/api/v1'

def registerPi(username, password):
	print('In registerPi')
	auth = HTTPBasicAuth(username, password)

	mac =1234999999999  # get_mac()
	print('mac: ' + str(mac))

	data = {'uuid': mac}
	raspi_resp = requests.post(
		URL_ROOT+'/raspberry_pi/?format=json',
		data=json.dumps(data),
		headers={'Content-type': 'application/json'},
		auth=auth
	)

	print('raspi_resp: ')
	print(raspi_resp)

	if raspi_resp.status_code not in [201,200]:
		print('raspi_resp not in [201,200]')
		print(raspi_resp)
		print(raspi_resp.json())
		return False

	return True

def defaultComponentRegistration(username,password):
	print('In defaultComponentRegistration.')
	auth = HTTPBasicAuth(username,password)
	userResponse = requests.get(URL_ROOT+'/user/?format=json',auth=auth)
	allUserInfo = userResponse.json()
	user = allUserInfo['objects'][0]
	raspberryPi = user['raspberry_pi'][0]
	headers = {'Content-type':'application/json'}

	data = {'raspberry_pi_id':raspberryPi['id'],'status':False,'gpio':4,'label':'Light One'}

	light_response = requests.post(URL_ROOT+'/light/?format=json',data=json.dumps(data),headers=headers,auth=auth)
	print('Light 1')
	print(light_response)
	print(light_response.json())

	data['gpio'] = 24
	data['label'] = 'Front Door'

	entrance_response = requests.post(URL_ROOT+'/entrance/?format=json',data=json.dumps(data),headers=headers,auth=auth)
	print('Entrance 1')
	print(entrance_response)
	print(entrance_response.json())
