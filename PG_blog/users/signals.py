from django.db.models.signals import post_save
from .models import NewUser,Profile
from django.dispatch import receiver

@receiver(post_save,sender=NewUser)
def create_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save,sender=NewUser)
def create_profile(sender,instance,**kwargs):
    instance.profile.save()