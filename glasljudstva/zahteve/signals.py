from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.conf import settings

from django_comments.models import Comment
# from django_comments.signals import comment_was_posted

from zahteve.utils import id_generator, send_email

from zahteve.models import EmailVerification

# @receiver(comment_was_posted, comment=None, request=None, **kwargs)
# def confirm_comment(comment, request, **kwargs):


@receiver(post_save, sender=Comment)
def copy_date_fields(sender, **kwargs):
    obj = kwargs['instance']
    created = kwargs['created']

    if created:
        obj.is_removed = True
        obj.save()


@receiver(post_save, sender=User)
def handle_social_users(sender, instance, created, **kwargs):
    if created:
        not_unique = True
        while not_unique:
            key_gen = id_generator(size=32)
            not_unique = EmailVerification.objects.filter(verification_key=key_gen)
            if not not_unique:
                EmailVerification(
                    verification_key=key_gen,
                    user=instance
                ).save()
                url = f'{settings.FRONT_URL}potrdi-naslov/{key_gen}/'
                send_email(
                    'Potrdi prijavo za glas ljudstva.',
                    instance.email,
                    'emails/email_verification.html',
                    {'url': url}
                )
                break
