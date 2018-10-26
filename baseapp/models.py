from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars', default='/default/user.png')
    about_me = models.TextField(max_length=280)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Interest(models.Model):
    user_interested = models.ManyToManyField(User, through='Interested', related_name='interests')
    name = models.CharField(max_length=255)
    thumbnail = models.ImageField(upload_to='interest_images', default='/default/thinking_emoji.png')
    INTEREST_TYPES = (
        ('M', 'Movie'),
        ('A', 'Anime'),
        ('B', 'Book'),
        ('G', 'Games'),
        ('S', 'Series'),
        ('O', 'Other')
    )
    interest_type = models.CharField(max_length=1, choices=INTEREST_TYPES)

    class Meta:
        unique_together = ('name', 'interest_type',)

    def full_type(self):
        return dict(Interest.INTEREST_TYPES)[self.interest_type]

    def search_link(self):
        engines = {
            'A': 'https://myanimelist.net/anime.php?q=',
        }
        url = engines.get(self.interest_type, '')
        if url:
            url += self.name
        return url

    def __str__(self):
        return f'({self.interest_type}) {self.name}'


class Interested(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    super_like = models.BooleanField(default=False)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.user} - {self.interest.name}  {"+++" if self.super_like else ""}'
