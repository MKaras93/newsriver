from django.core.management.base import BaseCommand, CommandError
from newsfeed.utils import *


class Command(BaseCommand):
    help = 'Loads new data from news api'

    def add_arguments(self, parser):
        parser.add_argument('q', nargs='*', type=str, default='news')

    def handle(self, *args, **options):
        q = options['q'][0]
        qlist = q.split(', ')

        res_msg = fetch_articles(q_list=qlist)
        self.stdout.write(self.style.SUCCESS(res_msg))
