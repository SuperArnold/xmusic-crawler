import unittest
import configparser
import uuid
import sys
sys.path.append('../')

from config import Config
from rpcservice.dbservice import DBService

config = Config("../xmusic.cfg")
print(config.db_host)
