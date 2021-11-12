from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail

from django_comments.models import Comment
from zahteve.utils import id_generator, send_email

from zahteve.models import EmailVerification


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
                send_mail(
                    'Potrdi prijavo za glas ljudstva.',
                    f'S klikom na povezavo potrdi',
                    settings.FROM_EMAIL,
                    [instance.email],
                    fail_silently=False,
)
                break
