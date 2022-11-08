from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from zahteve.models import Party, Election, Municipality
from zahteve.mautic_api import MauticApi
import time

EMAIL_TEMPLATE_ID = 11
mautic_api = MauticApi(username=settings.MAUTIC_USER, password=settings.MAUTIC_PASSWORD, url=settings.MAUTIC_URL)

def send_email(email_id, contact_id, municipality, username):
    """
    send_email to contact
    arguments:
        email_id: mautic email id
        contact_id: mautic contact id
        municipality: municipality name
    """
    response, response_status = mautic_api.sendEmail(
        email_id=email_id,
        contact_id=contact_id,
        data={
            'tokens': {
                'municipality': municipality,
                'username': username
            }
        })
    return response_status


class Command(BaseCommand):
    help = 'Send emails to candidates for 2022 local elections'

    def handle(self, *args, **options):
        election = Election.objects.get(slug='lokalne-volitve-2022')
        parties = Party.objects.filter(election=election, mautic_id__isnull=False).exclude(email="")

        count = parties.count()
        self.stdout.write(f'Found {count} parties')

        time.sleep(5)

        self.stdout.write(f'Sending emails...')

        i = 0
        for party in parties:
            i += 1

            self.stdout.write(f'Sending to {i}/{count} "{party.party_name}" mautic id = {party.mautic_id}')
            time.sleep(1)
            response_status = send_email(email_id=EMAIL_TEMPLATE_ID, contact_id=party.mautic_id, municipality=party.municipality.name, username=party.user.username)
            self.stdout.write(f'Status: {response_status}')
            self.stdout.write('---')

        self.stdout.write('DONE')
