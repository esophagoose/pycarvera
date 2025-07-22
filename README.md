# Python Carvera

A Python CLI and library for interacting with Makera Carvera CNC machines.

## Features

- **Connect to Carvera machines via USB or WiFi**
- **List available Carvera machines on your network or connected via USB**

## Command Line Usage
```
> pycarvera --list
```
This will scan for USB devices and your local network for Carvera machines. You can always select a connection type using `--connection` or `-c` like this: 
```
> pycarvera -c wifi --list
```

Carvera machines will be printed to console:
```
Found 1 Carvera machines:
  1: [CARVERA_AIR] 192.168.1.6:2222
```





