import enum
import hashlib
import os
import re
import socket
from collections import namedtuple

import serial
import serial.tools.list_ports
import xmodem


class ConnectionError(Exception):
    pass


class ConnectionNotReadyError(ConnectionError):
    pass


Carvera = namedtuple("Carvera", ["name", "address", "busy"])


def get_connector_from_address(address: str) -> "Connection":
    ip_pattern = r"([0-9]+|\.){8}:\d+"
    if os.path.exists(address):
        return UsbConnection().open(address)
    elif re.match(ip_pattern, address):
        return WifiConnection().open(address)
    raise ValueError(f"Invalid address: {address}")


class Connection:

    def __init__(self):
        self.modem = xmodem.XMODEM(self._recv, self._send, "xmodem8k")
        self.ready = False

    def find(self) -> list[Carvera]:
        raise NotImplementedError

    def open(self, address: str) -> "Connection":
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def send(self, data: str | bytes):
        if not self.ready:
            raise ConnectionNotReadyError("Did you open the device?")
        if isinstance(data, str):
            data = data.encode("utf-8")
        self._send(data)

    def _send(self, data: bytes):
        raise NotImplementedError

    def recv(self) -> str:
        if not self.ready:
            raise ConnectionNotReadyError("Did you open the device?")
        response = self._recv()
        if response.endswith(xmodem.EOT.decode()):
            return response[:-1]
        return response

    def _recv(self) -> str:
        raise NotImplementedError

    def upload(self, filename: str) -> bool:
        with open(filename, "rb") as f:
            data = f.read()
            md5_hash = hashlib.md5(data).hexdigest().encode()
            response = self.modem.send(md5_hash + data)
            return response

    def download(self, filename: str) -> bool:
        with open(filename, "wb") as f:
            response = self.modem.recv(f)
            return response


class WifiConnection(Connection):
    TCP_PORT = 2222
    UDP_PORT = 3333
    UDP_IP = "0.0.0.0"
    DEFAULT_TIMEOUT = 1.0

    def __init__(self):
        super().__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(self.DEFAULT_TIMEOUT)
        self.connected = False

    def find(self) -> list[Carvera]:
        machines = []
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(5)
            sock.bind((self.UDP_IP, self.UDP_PORT))
            try:
                data, _ = sock.recvfrom(128)
                name, ip, port, busy = data.decode("utf-8").split(",")
                machines.append(Carvera(name, f"{ip}:{port}", bool(int(busy))))
            except socket.timeout:
                pass
        return machines

    def open(self, address: str):
        """Open WiFi connection to the machine."""
        try:
            address, _, port_str = address.partition(":")
            port = int(port_str) if port_str else self.TCP_PORT
            self.socket.connect((address, port))
            self.ready = True
        except socket.error as e:
            print(f"WiFi connection failed: {e}")
        return self

    def close(self):
        """Close WiFi connection."""
        if self.socket:
            self.socket.close()

    def _send(self, data: bytes):
        self.socket.sendall(data)

    def _recv(self):
        """Receive data from the machine."""
        return self.socket.recv(4096).decode()


class UsbConnection(Connection):
    DEFAULT_BAUDRATE = 115200
    DEFAULT_TIMEOUT = 1.0
    VID = 0x0403
    PID = 0x6001

    def __init__(self):
        super().__init__()
        self.serial = None
        self.device = None

    def find(self) -> list[Carvera]:
        machines = []
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if port.vid == self.VID and port.pid == self.PID:
                machines.append(Carvera(port.interface, port.device, False))
        return machines

    def open(self, address: str):
        """Open USB connection to the machine."""
        self.device = address
        self.serial = serial.Serial(
            port=address,
            baudrate=self.DEFAULT_BAUDRATE,
            timeout=self.DEFAULT_TIMEOUT,
            write_timeout=self.DEFAULT_TIMEOUT,
        )
        self.serial.flush()
        self.ready = True
        return self

    def _send(self, data):
        self.serial.write(data)

    def _recv(self):
        return self.serial.read()

    def flush(self):
        if not self.serial or not self.serial.is_open:
            raise ConnectionNotReadyError("Serial port not open")
        self.serial.flush()


class ConnectionType(enum.Enum):
    USB = UsbConnection
    WIFI = WifiConnection
