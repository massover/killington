from django.core.management.base import BaseCommand
from ...factories import ShowFactory, UserFactory


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('model', nargs='+', type=str)

    def handle(self, *args, **options):
        if 'shows' in options['model']:
            ShowFactory(name='Aladdin',
                        url='https://lottery.broadwaydirect.com/show/aladdin/')
            ShowFactory(
                name='Cats', url='https://lottery.broadwaydirect.com/show/cats/')
            ShowFactory(name='Hamilton',
                        url='https://lottery.broadwaydirect.com/show/hamilton/')
            ShowFactory(name='On Your Feet',
                        url='https://lottery.broadwaydirect.com/show/on-your-feet/')
            ShowFactory(name='The Lion King',
                        url='https://lottery.broadwaydirect.com/show/the-lion-king/')
            ShowFactory(name='Wicked',
                        url='https://lottery.broadwaydirect.com/show/wicked/')
            self.stdout.write('Created 6 Shows')

        if 'users' in options['model']:
            UserFactory(email='admin@example.com',
                        is_staff=True, is_superuser=True)
            self.stdout.write('Created 1 User')
