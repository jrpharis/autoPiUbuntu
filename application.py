import os
import json
import requests
from requests.auth import HTTPBasicAuth

URL_ROOT = 'http://autopi.herokuapp.com/api/v1'
prevLights = {}

prevEntrances = None

def start(username,password):
	print 'username: ' + username + ' password: ' + password
	auth=HTTPBasicAuth(username,password)
	user = getUser(auth)
	raspberryPi = getPi(user)
	lights = getLights(auth)
	entrances = getEntrances(auth)

	while True:
		lights = getLights(auth)
		updateLights(lights)
		
		updateEntrances(entrances,auth,raspberryPi['id'])
	

def updateLights(lights):
	for light in lights:
		gpioPin = light['gpio']	
		print gpioPin
		print light['status']
		if light['status'] == True:
			print 'Light turned on'
		else:
			print 'Light turned off'

def updateEntrances(entrances,auth,PiID):
	global prevEntrances

	statusValues = {1:True,0:False}

	currentEntranceStatus = 0
	print 'CurrentStatus'
	print currentEntranceStatus
	if currentEntranceStatus != prevEntrances:
		print'Status has changed'
		prevEntrances = currentEntranceStatus
		entranceID = entrances['id']

		params = {
			'raspberry_pi_id':PiID,
			'status':statusValues[currentEntranceStatus]}

		updateResponse = requests.put(
			'%s/entrance/%s/?format=json' % (URL_ROOT, entranceID),
			data = json.dumps(params),
			headers={'Content-type':'application/json'},
			auth=auth,
		)

		print 'updateResponse'
		print updateResponse

def getUser(auth):
	userResponse = requests.get(URL_ROOT+'/user/?format=json',auth=auth)
	allUserInfo = userResponse.json()
	user = allUserInfo['objects'][0]

	return user

def getPi(user):
	raspberryPi = user['raspberry_pi'][0]

	return raspberryPi

def getLights(auth):
	lightsResponse = requests.get(URL_ROOT+'/light/?format=json',auth=auth)
	light_count = lightsResponse.json()['meta']['total_count']

	lights = lightsResponse.json()['objects']

	return lights

def getEntrances(auth):
	entrancesResponse = requests.get(URL_ROOT+'/entrance/?format=json',auth=auth)
	entrance_count = entrancesResponse.json()['meta']['total_count']
	print entrancesResponse.json()
	entrances = entrancesResponse.json()['objects'][0]


	return entrances
