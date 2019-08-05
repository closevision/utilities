#!/usr/bin/env python

__author__ = "Maros Kukan"
__author_email__ = "maros.kukan@me.com"
__license__ = "GPL"

from datetime import datetime
from multiprocessing import Process, Queue

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

def ping_address(host, queue):
    """ Check if host is reachable, if yes, use queue to pass it back ot main process
    :param host: single IPv4 Address objects
    :param queue: queue object
    """
    option = '-n' if sys.platform == 'win32' else '-c'
    try:
        response = subprocess.check_output(['ping', option, '1', str(host)])
        if ('Reply from ' + str(host)) in response.decode('utf-8'):
            queue.put(host)
        else:
            pass
    except subprocess.CalledProcessError:
        pass

def print_results(queue):
    """ Iterate through list of reachable IPv4 address objects and print them on screen.
    :param queue: a queue containing reachable IPv4 Address objects
    """
    if queue.empty():
        print('There is zero reachable addresses in selected network.')
    else:
        print('The following hosts are reachable.\n')
        while not queue.empty():
            print(queue.get())

def main():
    """ Use process to ping each address in CIDR range. Use queue to pass the reachable
    address back to parent process. Wait for all process completion. Print the results.
    Record the amount of time to complete the task.
    """
    addresses = get_address()
    startTime = datetime.now()

    queue = Queue()

    processes = [Process(target=ping_address, args=(address, queue)) for address in addresses]

    for process in processes:
        process.start()

    for process in processes:
        process.join() 

    # Alternative solution  
    # queue = Queue()
    # procs = []
    # for address in addresses:
    #     my_proc = Process(target=ping_address, args=(address, queue))
    #     my_proc.start()
    #     procs.append(my_proc)
    # for a_proc in procs:
    #     a_proc.join()

    print_results(queue)
    
    endTime = datetime.now() - startTime
    print('\nScript completed in {}.'.format(endTime))

if __name__ == '__main__':
    main()