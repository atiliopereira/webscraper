from django.contrib.auth.models import Permission, User
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def add_permissions_to_new_user(sender, instance, created, **kwargs):
    if created:
        permission = Permission.objects.get(name="Can view page")
        instance.user_permissions.add(permission)
        instance.is_staff = True
        instance.save()
