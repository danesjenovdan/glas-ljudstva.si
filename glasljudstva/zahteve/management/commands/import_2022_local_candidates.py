from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.conf import settings
from zahteve.models import Party, Election, Municipality
from zahteve.mautic_api import MauticApi
import os
import json

# TODO: dodaj wait med pošiljanjem mejlov v loopu
# TODO: send_email(email_id=EMAIL_TEMPLATE_ID, contact_id=151, municipality='Test123', username="Testniuser123")

# TODO: segment prod = 4
SEGMENT_ID = 5
EMAIL_TEMPLATE_ID = 10
mautic_api = MauticApi(username=settings.MAUTIC_USER, password=settings.MAUTIC_PASSWORD, url=settings.MAUTIC_URL)

def add_user_to_mautic(email, name, password, segment_id):
    """
    add user to mautic
    arguments:
        email
        name
        password
    returns:
        if success
            mautic_id
        else
            None
    """
    response_contact, response_status = mautic_api.createContact(
        email=email,
        name=name,
        password=password
    )
    if response_status == 200:
        mautic_id = response_contact['contact']['id']
        response, response_status = mautic_api.addContactToASegment(segment_id, mautic_id)
        return mautic_id
    else:
        return None

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
    help = 'Create users and parties for 2022 local elections'

    def handle(self, *args, **options):
        election = Election.objects.get(slug='lokalne-volitve-2022')

        self.stdout.write(f'Creating users and parties...')

        with open(os.path.join(os.path.dirname(__file__), 'users_to_import.json'), 'r') as f:
            users = json.load(f)
            count = len(users)
            self.stdout.write(f'Loaded {count} users')

            usernames = list(map(lambda x: x['username'], users))
            existing = User.objects.filter(username__in=usernames)
            if existing:
                self.stdout.write('---')
                self.stdout.write(f'{existing.count()} existing users!!')
                self.stdout.write(', '.join(existing.values_list('username', flat=True)))
                self.stdout.write('--- Exiting')
                return

            i = 0
            for user in users:
                i += 1
                self.stdout.write(f'Creating user {i}/{count} "{user["name"]}"')

                m = Municipality.objects.get(name=user['municipality'])
                u = User.objects.create_user(
                    username=user['username'],
                    password=user['password'],
                )
                mautic_id = add_user_to_mautic(user['email'], user['name'], password=user['password'], segment_id=SEGMENT_ID)
                p = Party.objects.create(
                    user=u,
                    party_name=user['name'],
                    proposer=user['proposer'],
                    sex=user['gender'],
                    email=user['email'],
                    election=election,
                    municipality=m,
                    already_has_pp=user['already_has_pp'],
                    mautic_id=mautic_id if mautic_id else None
                )

                self.stdout.write('---')

        self.stdout.write('DONE')
