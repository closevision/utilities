#!/usr/bin/env python

from datetime import datetime
import ipaddress
import subprocess
import sys


def get_address():
    """ Ask user for valid CIDR address (e.g. 192.168.0.0/24) and return a list of IPv4 Addresses
    :return: a list of IPv4 Address objects
    """
    while True:
        try:
            network = ipaddress.ip_network(input('Enter network address in CIDR format: '))
            break
        except:
            print('Error: The entered address is invalid.')
    hosts = list(network.hosts())
    return hosts

def ping_address(hosts):
    """ Iterate through list of IPv4 address objects and return a list with reachable addreses.
    :param hosts: a list of IPv4 Address objects
    :return: a list of reachable IPv4 Address objects
    """
    reachable_hosts = []
    option = '-n' if sys.platform == 'win32' else '-c'
    for host in hosts:
        try:
            response = subprocess.check_output(['ping', option, '1', str(host)])
            if ('Reply from ' + str(host)) in response.decode('utf-8'):
                #print('{} is reachable.'.format(host))
                reachable_hosts.append(host)
            else:
                pass
                #print('{} is unreachable.'.format(host))
        except subprocess.CalledProcessError:
            pass
            #print('{} is unreachable.'.format(host))
    return reachable_hosts

def print_results(reachable_hosts):
    """ Iterate through list of reachable IPv4 address objects and prints them on screen.
    :param reachable_hosts: a list of reachable IPv4 Address objects
    """
    if not reachable_hosts:
        print('There is zero reachable addresses in selected network.')
    else:
        print('The following hosts are reachable.\n')
        for host in reachable_hosts:
            print(host)

def main():
    """ Records the start of the script, ask user for network CIDR address, 
    check reachability for each host serially, print the result and script
    run time.
    """
    startTime = datetime.now()
    
    # Asks user for network address, checks reachability and prints the resulsts
    print_results(ping_address(get_address()))

    endTime = datetime.now() - startTime
    print('\nScript completed in {}.'.format(endTime))

if __name__ == '__main__':
    main()