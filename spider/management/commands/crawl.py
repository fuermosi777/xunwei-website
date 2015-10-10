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
            try:
                ss = importlib.import_module('spider.xxx.%s'%args[0])
            except:
                print "No spider"
                return
            ss.start()
        else:
            pass