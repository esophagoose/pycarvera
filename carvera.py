import datetime
import logging
import os
import pathlib
from typing import NamedTuple

from connectors import Connection

LOG = logging.getLogger(__name__)

REMOTE_GCODE_DIR = pathlib.Path("/sd/gcodes")


def escape(string: str):
    string = string.replace(" ", "\x01").replace("\\", "/")
    string = string.replace("?", "\x02").replace("*", "\x03")
    return string.replace("!", "\x04").replace("~", "\x05")


class FileInfo(NamedTuple):
    name: str
    size: int
    date: datetime.datetime

    def __str__(self):
        readable_size = self.size
        units = ["B", "KB", "MB", "GB", "TB"]
        for unit in units:
            if readable_size < 1000:
                break
            readable_size /= 1000
        return f"{self.name} ({readable_size:.2f} {unit})"


class CarveraController:

    def __init__(self, connection: Connection):
        self.connection = connection

    def run(self, command: str):
        self.connection.send(command)

    def list_files(self, directory: pathlib.Path = REMOTE_GCODE_DIR):
        files = []
        self.run(f"ls -e -s {escape(str(directory))}\n")
        for line in self.connection.recv().splitlines():
            name, size, date = line.split()
            date = datetime.datetime.strptime(date, "%Y%m%d%H%M%S")
            files.append(FileInfo(name=name, size=int(size), date=date))
        return files

    def remove_file(self, filename: pathlib.Path):
        self.run(f"rm {escape(str(filename))}\n")

    def upload(self, filepath: str):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Upload file not found: {filepath}")
        self.run(f"upload {escape(filepath)}\n")
        self.connection.upload(filepath)
