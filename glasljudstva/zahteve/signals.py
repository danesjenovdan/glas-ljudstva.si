from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from django_comments.models import Comment

@receiver(post_save, sender=Comment)
def copy_date_fields(sender, **kwargs):
    obj = kwargs['instance']
    created = kwargs['created']

    if created:
        obj.is_removed = True
        obj.save()
