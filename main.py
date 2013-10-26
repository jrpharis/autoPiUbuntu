from Tkinter import *
from application import *
from autoPiStartup import *
import tkMessageBox
from register import *
import requests
import os
import json

URL_ROOT = 'http://autopi.herokuapp.com/api/v1'

class App:
	def __init__(self, master):
		self.homepath = os.environ['HOME']
		frame = Frame(master)
		frame.pack()
		Label(frame, text='Username').grid(row=0, column=0)
		self.username = StringVar()
		Entry(frame, textvariable=self.username).grid(row=0,column=1)
		Label(frame, text='Password').grid(row=1, column=0)
		self.password = StringVar()
		Entry(frame, textvariable=self.password).grid(row=1, column=1)
		login_button = Button(frame, text='Login', command=self.getUser)
		login_button.grid(row=2)

	def getUser(self):
		print('In getUser()')
		try:
			login_response = requests.get(URL_ROOT + '/user/?format=json',auth = HTTPBasicAuth(self.username.get(),self.password.get()))
		except:
			setNoInternetError()
			return

		if login_response.status_code not in [200,201]:
			setLoginError()
			return 

		SaveUser(homepath,self.username.get(),self.password.get())

		root.quit()		
		return


def login(username, password):
	print('Logging in: username-' + username + ' password-' + password)
	try:
		login_response = requests.get(URL_ROOT + '/user/?format=json',auth = HTTPBasicAuth(username,password))
	except:
		setNoInternetError()
		return

	return login_response

def setNoInternetError():
#	tkMessageBox.showinfo('Error','No internet')
	print('No internet')

def setLoginError():
#	tkMessageBox.showinfo('Error','Login failed')
	print('Login error')

def setRegisterError(component):
	tkMessageBox.showinfo('Error','Could not register ' + component + 'component.')





homepath = os.environ['HOME']

config_exists = os.path.exists(homepath + '/autopi.config')

if config_exists != True:
	print('autopi.config doesn''t exist. Creating.')
	createConfig(homepath)

if UserSaved(homepath) == True:
	print('UserSaved() == True')
	config = ConfigParser.ConfigParser()
	config.read(homepath+'/autopi.config')
	username = config.get('LoginInfo','username')
	password = config.get('LoginInfo','password')

	username ='test5'
	password = 'test'
	
	print('Username: ' + username)
	print('Password: ' + password)
	
	login_success = login(username,password)
	print('Login: ')
	print(login_success)
	print login_success.json()

	if login_success.status_code not in [200,201]:
		print('Login status code not in [200,201]')
		setLoginError()
		exit()

	all_user_info = login_success.json()
	user = all_user_info['objects'][0]

	print(user['raspberry_pi'])
	if user['raspberry_pi'] == []:
		print('No Raspberry Pi for user')
		register_success = registerPi(username,password)

		if register_success == False:
			setRegisterError('Pi')
			exit()

		defaultComponentRegistation(username,password)

else:
	print('User not saved')
	root = Tk()
	root.wm_title('AutoPi Login')
	app = App(root)
	root.mainloop()

	config = ConfigParser.ConfigParser()
	config.read(homepath+'/autopi.config')
	username = config.get('LoginInfo','username')
	password = config.get('LoginInfo','password')

	print('username: ' + username)
	print('password: ' + password)
	register_success = registerPi(username,password)
	print('register_success:')
	print(register_success)

	if register_success == False:
		setRegisterError('Pi')
		exit()

	defaultComponentRegistration(username,password)

start(username,password)
