#!/usr/bin/env python

import ipaddress
import random
import sys


def scalc():
    try:
        # IPv4 address and mask length validation
        while True:
            try:
                host = ipaddress.IPv4Interface(input('\nEnter an IPv4 address in CIDR format: '))

                # Address type validation
                if not (host.is_loopback or host.is_multicast or host.is_reserved):
                    break
                else:
                    print('\nThe IP address is loopback, multicast or reserved. Try again!\n')
            except ValueError:
               print('\nThe IP address or mask is invalid. Please try again!\n')
               continue

        # Generating results for entered address
        ipaddr, network, prefixlen = host.ip, host.network, host._prefixlen
        netmask, wildmask = host.netmask, host.hostmask
        validHosts = [host for host in network.hosts()]
        maxHosts = len(validHosts)
        # Another, less accurate approach maxHosts = abs((network.num_addresses) - 2)

        # Printing results
        print('\n  {:38}{:38}'.format('Result','Value'))
        print('+{}+'.format('-' * 78))
        print('| {:38}{:38} |'.format('IP Address:', str(ipaddr)))
        print('| {:38}{:38} |'.format('Network Address:', str(network)))
        print('| {:38}{:38} |'.format('Network Mask:', str(netmask)))
        print('| {:38}{:38} |'.format('Wildcard mask:', str(wildmask)))
        print('| {:38}{:38} |'.format('Prefix length:', str(prefixlen)))
        print('| {:38}{:38} |'.format('Max hosts in network:', str(maxHosts)))
        print('+{}+'.format('-' * 78))

    except KeyboardInterrupt:
        print('\nAborted by user. Exiting...\n')
        sys.exit()

if __name__ == '__main__':
    while True:
        scalc()
        print('\nCalculate another address? (Yes/No)')
        if not input().lower().startswith('y'):
            break
