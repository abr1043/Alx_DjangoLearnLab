from django.db import models
from django.contrib.auth.models import AbstractUser


def profile_image_upload_to(instance, filename):
    # This function defines the upload path for user profile pictures
    return f'profile_pics/{instance.username}/{filename}'


class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to=profile_image_upload_to,
        blank=True,
        null=True
    )
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        blank=True
    )

    def __str__(self):
        return self.username
