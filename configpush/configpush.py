#!/usr/bin/env python

from __future__ import print_function
import getpass
import json
import netmiko
import signal
import sys

signal.signal(signal.SIGINT, signal.SIG_DFL)

netmiko_exceptions = (netmiko.ssh_exception.NetMikoTimeoutException,
                      netmiko.ssh_exception.NetMikoAuthenticationException)


def get_input(prompt=''):
    '''
    Reads user specified input and returns it as string. Provides
    backward compatibility with Pyhon2.
    '''
    try:
        line = raw_input(prompt)
    except NameError:
        line = input(prompt)
    return line

def get_creds():
    '''
    Asks for username and verified password and returns them.
    '''
    username = get_input('Enter your username: ')
    password = None
    while not password:
        password = getpass.getpass('Enter your password: ')
        password_verify = getpass.getpass('Retype your password: ')
        if password != password_verify:
            print('Passwords do not match. Try again!')
            password = None
    return username, password

def load_devices(devfile):
    '''
    Loads user specified json file that contains a list of devices and 
    returns a dictionary.
    '''
    try:
        with open(devfile) as dev_file:
            devices = json.load(dev_file)
            print('\033[92m'+ 'Success: {} loaded.'.format(devfile) + '\033[0m')
            return devices
    except FileNotFoundError:
        print('\033[91m' + 'Error: Unable to load {}'.format(devfile) + '\033[0m')
        sys.exit(1)

def load_commands(cmdfile):
    '''
    Loads user specified text file that contains a list of commands, one
    on each line. Retuns a list of these commands.
    '''
    try:
        with open(cmdfile) as cmd_file:
            commands = cmd_file.readlines()
            print('\033[92m'+ 'Success: {} loaded.'.format(cmdfile) + '\033[0m')
            return commands
    except FileNotFoundError:
            print('\033[91m' + 'Error: Unable to load {}'.format(cmdfile) + '\033[0m')
            sys.exit(1)

def configpush():
    if len(sys.argv) < 3:
        print('Usage: {} <devices> <commands>'.format(sys.argv[0],))
        sys.exit(0)

    # Load Device and Command List
    devices = load_devices(sys.argv[1])
    commands = load_commands(sys.argv[2])

    # Retrieve username and password
    username, password = get_creds()

    # For each device execute commands
    for device in devices:
        device['username'] = username
        device['password'] = password
        role = device.pop('role')

        try:
            print('#' * 80, '\n')
            print('Connecting to {}...'.format(device['ip']))
            connection = netmiko.ConnectHandler(**device)
            print('Connected to {} switch {}\n'.format(role, connection.base_prompt))
            
            for command in commands:
                print('## Output of {}\n'.format(command))
                print(connection.send_command(command))

            print('Disconnecting...')
            connection.disconnect()
        except netmiko_exceptions as e:
            print('Failed to {} {}'.format(device['ip'],e))


if __name__ == '__main__':
    configpush()