# notifications/signals.py
from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.conf import settings

from posts.models import Like, Comment, Post
from django.contrib.auth import get_user_model

from .models import Notification

User = get_user_model()

def create_notification(recipient, actor, verb, target=None, description=None):
    content_type = None
    object_id = None
    if target is not None:
        content_type = ContentType.objects.get_for_model(target.__class__)
        object_id = str(getattr(target, 'pk', None))
    Notification.objects.create(
        recipient=recipient,
        actor=actor,
        verb=verb,
        description=description or '',
        target_content_type=content_type,
        target_object_id=object_id
    )

# When a Like is created -> notify post author
@receiver(post_save, sender=Like)
def like_created(sender, instance, created, **kwargs):
    if created:
        post = instance.post
        actor = instance.user
        recipient = post.author
        if recipient != actor:
            create_notification(recipient=recipient, actor=actor, verb='liked your post', target=post)

# When a Comment is created -> notify post author
@receiver(post_save, sender=Comment)
def comment_created(sender, instance, created, **kwargs):
    if created:
        post = instance.post
        actor = instance.author
        recipient = post.author
        if recipient != actor:
            create_notification(recipient=recipient, actor=actor, verb='commented on your post', target=post, description=instance.content)

# Optional: Follow notifications — if you implement follow via a signal or call create_notification where follow happens.
