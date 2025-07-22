#!/usr/bin/env python3
"""
Makera Carvera CLI
A command-line interface for controlling Makera Carvera CNC machines.
"""

import argparse
import enum

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
    return parser


def main():
    parser = arg_parser()
    args = parser.parse_args()

    print("\n✨ Makera Carvera CLI ✨\n")

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

    print("No options specified, use --help for usage\n")


if __name__ == "__main__":
    main()
