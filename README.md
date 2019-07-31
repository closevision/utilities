# Utilities
Various handy scripts.

## Scalc
Subnet calculator utilizing ipaddress module.

## Configpush
Config pusher reads device list defined in json and uses Netmiko to execute commands in a configuration file.

## Configloader
Config loader can be used as module to load external configuration and credentials from an external .ini file. 
To do so it leverges the existing configparser module. 

## Eping
Uses sys to determine the OS and subprocess module to call ping program to validate reachbility for give CIDR address block.
Validates address one by one which can take lot of time to complte.
