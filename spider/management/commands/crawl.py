import sys
from django.core.management.base import BaseCommand, CommandError
from api.models import *
from datetime import datetime, timedelta
from multiprocessing import Pool
from django.db import connection
import importlib

class Command(BaseCommand):
    help = ""
    args = '<test>'
    def handle(self, *args, **options):
        
        if args:
            ss = importlib.import_module('spider.xxx.%s'%args[0])
            ss.start()
        else:
            vendor = ['bigapple', 'chihuo', 'sinovision', 'wocao']
            for v in vendor:
                ss = importlib.import_module('spider.xxx.%s'%v)
                ss.start()