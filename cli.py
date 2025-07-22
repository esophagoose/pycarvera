#!/usr/bin/env python3
"""
Makera Carvera CLI
A command-line interface for controlling Makera Carvera CNC machines.
"""

import argparse

import carvera
import connectors as conn_lib


def arg_parser():
    parser = argparse.ArgumentParser(description="Makera Carvera CLI")
    parser.add_argument("-c",
                        "--connection",
                        type=str,
                        choices=["usb", "wifi"])
    parser.add_argument("--list",
                        action="store_true",
                        help="List available Carvera machines")
    parser.add_argument("-a", "--address", type=str, help="Carvera address")
    parser.add_argument(
        "-f",
        "--list_remote_files",
        action="store_true",
        help="List files on the Carvera",
    )
    return parser


def main():
    parser = arg_parser()
    args = parser.parse_args()

    print("\n\033[1m✨ Makera Carvera CLI ✨\033[0m\n")

    if args.list:
        connectors = [e.value() for e in conn_lib.ConnectionType]
        if args.connection:
            conn_type = args.connection.upper()
            connectors = [conn_lib.ConnectionType[conn_type].value()]

        devices = []
        for connector in connectors:
            devices.extend(connector.find())
        print(f"Found {len(devices)} Carvera machines:")
        for i, device in enumerate(devices):
            print(f"  {i+1}: [{device.name}] {device.address}")
        print()
        return

    if not args.address:
        print("No address specified, use --help for usage\n")
        return

    if args.list_remote_files:
        connector = conn_lib.get_connector_from_address(args.address)
        machine = carvera.CarveraController(connector)
        files = machine.list_files()
        print(f"{len(files)} gcode files found on the Carvera:")
        for i, filename in enumerate(files):
            print(f"  {i+1}: {filename}")
        print()
        return

    print("No options specified, use --help for usage\n")


if __name__ == "__main__":
    main()
