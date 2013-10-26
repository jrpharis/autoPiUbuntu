import os
import ConfigParser

def UserSaved(path):
	config = ConfigParser.ConfigParser()
	config.read(path+'/autopi.config')

#check that LoginInfo section exists, create and 
#retrun false if no LoginInfo section
	if ('LoginInfo' in config.sections()) != True:
		config.add_section('LoginInfo')
		config_file = open(path+'/autopi.config','w')
		config.write(config_file)
		config_file.close()
		return False 

	if (config.has_option('LoginInfo', 'username') or config.has_option('LoginInfo','password')) != True:
		return False

	return True

def createConfig(path):
	open(path+'/autopi.config','w').close()

def SaveUser(path,username,password):
	print('In autoPiStartup.SaveUser')
	config = ConfigParser.ConfigParser()
	config.read(path+'/autopi.config')
	config_file = open(path+'/autopi.config','w')
	config.set('LoginInfo','Username',username)
	config.set('LoginInfo','Password',password)
	config.write(config_file)
	config_file.close()
	return True
