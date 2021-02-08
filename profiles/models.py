from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django_countries.fields import CountryField
from django.core.validators import RegexValidator


class UserProfile(models.Model):
    """
    models.OneToOneField ensures each user
    only has one profile and each profile is
    only attatched to one person """
    # error message when a wrong format entered
    phone_message = 'Please enter valid phone number'

    # desired format
    phone_regex = RegexValidator(
        regex=r'^0([1-6][0-9]{8,10}|7[0-9]{9})$',
        message=phone_message
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # use null = True and blank = True to make optional

    default_name = models.CharField(max_length=25, null=False, blank=False,
                                    default='')
    # email is required by default
    default_email = models.EmailField(max_length=254, null=False, blank=False,
                                      default='')
    default_contact_number = models.CharField(validators=[phone_regex],
                                              max_length=60, null=False,
                                              blank=False, default='')

    default_street_address1 = models.CharField(max_length=80, null=False,
                                               blank=False, default='')

    default_street_address2 = models.CharField(max_length=80, null=True,
                                               blank=True)

    default_town = models.CharField(max_length=40, null=False,
                                    blank=False, default='')

    default_postcode = models.CharField(max_length=10, null=True,
                                        blank=True)

    default_counrty = CountryField(blank_label='Country *', null=False,
                                   blank=False)

    def __str__(self):
        return self.user


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    try:
        instance.userprofile.save()
    except ObjectDoesNotExist:
        UserProfile.objects.create(user=instance)
