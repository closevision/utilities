# Utilities
Various handy scripts.

## Scalc
Subnet calculator utilizing ipaddress module.

## Configpush
Config pusher reads device list defined in json and uses Netmiko to execute commands in a configuration file.

## Configloader
Config loader can be used as module to load external configuration and credentials from an external .ini file. 
To do so it leverges the existing configparser module. 

## eping

### eping-serial.py

Asks user for a block of IP addresses in CIDR format. Validates the input using ipaddress module. Generates a list of address and iterates each of them in loop.
Using process module calls out to ping binary and validates reachability of each address.
Finally prints all reachable addresses and records amount of time to complete.

Due to its serial nature and ping default timings takes significant amout of time
to complete. For example for Class-C network it may take up 7 minutes to finish.

*Example*
```
py .\eping-serial.py
Enter network address in CIDR format: 10.0.1.0/24
10.0.1.1
10.0.1.15
10.0.1.155
10.0.1.172
10.0.1.252

Script completed in 0:06:30.383892.
```

### eping-parallel.py

Similar to previous script, asks user for CIDR block. Generates a list of address but uses Process and Queue module to increase the processing speed significantly. Ordering is not applied to the result set automatically.

*Example*
```
py .\eping-parallel.py 
Enter network address in CIDR format: 10.0.1.0/24
The following hosts are reachable.

10.0.1.1
10.0.1.15
10.0.1.155
10.0.1.252
10.0.1.172

Script completed in 0:00:10.609903.
```