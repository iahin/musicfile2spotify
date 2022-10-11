import glob
import json
from logging import FileHandler
from pathlib import Path


class FileHandle:
    def __init__(self, pathlist) -> None:
        self.pathlist = pathlist
        self.musicnamelist = []

    def getmusiclist(self) -> list:
        print("Getting song list...")
        for datafiles in self.pathlist:
            self.musicnamelist.append(Path(datafiles).stem)
        return self.musicnamelist
