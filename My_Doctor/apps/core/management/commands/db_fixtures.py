import json

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    args = ''
    help = 'Load initial data to database'

    def handle(self, *args, **options):
        files = [
            'fixtures/category_data.json',
            'fixtures/user_data.json',
            'fixtures/director_data.json',
            'fixtures/doctor_data.json',
            'fixtures/patient_data.json',
            'fixtures/visit_data.json',
            'fixtures/imagefile_data.json',
        ]

        for file in files:
            call_command('loaddata', file, verbosity=0)

        result = {'message': "Successfully loaded initial data"}
        return json.dumps(result)    