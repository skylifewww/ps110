import os, sys
base = os.path.dirname(os.path.dirname(__file__))
base_parent = os.path.dirname(base)
sys.path.append(base)
sys.path.append(base_parent)

from django.core.management.base import BaseCommand, CommandError
import sys, os, time, random, time

from django.contrib.auth.models import User

os.environ['DJANGO_SETTINGS_MODULE'] = ''
from django.conf import settings

class Command(BaseCommand):
    help = 'Example command taking an argument from the command line and with access to model '

    def add_arguments(self, parser):
        parser.add_argument('user_id', nargs='+', type=int)

    def handle(self, *args, **options):
        for user_id in options['user_id']:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise CommandError('User "%s" does not exist' % user_id)



            # Add your code here, you have access to the model as seen above

            print "finish"
