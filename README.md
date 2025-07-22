# Python Carvera

A Python CLI and library for interacting with Makera Carvera CNC machines.

## Features

- Connect to Carvera machines via USB or WiFi
- List G-code files stored on the Carvera machine
- Remove G-code files from the Carvera machine

## Command Line Usage
### Finding Available Carvera Machines
```
> pycarvera --list
```
This will scan for USB devices and your local network for Carvera machines. You can always select a connection type using `--connection` or `-c` like this: 
```
> pycarvera -c wifi --list
```

Carvera machines will be printed to console:
```
✨ Makera Carvera CLI ✨

Found 1 Carvera machines:
  1: [CARVERA_AIR] 192.168.1.6:2222
```

### Listing Files on Your CNC
You can see what files are on your Carver using the `-a` option to give an address to your Carvera and the `-f` option to list files

```
> pycarvera -a 192.168.1.6:2222 -f

✨ Makera Carvera CLI ✨

1 gcode files found on the Carvera:
  1: PirateShip.nc (2.99 MB)

```


### Full Usage
```
usage: pycarvera [-h] [-c {usb,wifi}] [--list] [-a ADDRESS] [-f]

Makera Carvera CLI

options:
  -h, --help            show this help message and exit
  -c {usb,wifi}, --connection {usb,wifi}
  --list                List available Carvera machines
  -a ADDRESS, --address ADDRESS
                        Carvera address
  -f, --list_remote_files
                        List files on the Carvera
  -r REMOVE_FILE, --remove_file REMOVE_FILE
                        Remove a file from the Carvera
```


