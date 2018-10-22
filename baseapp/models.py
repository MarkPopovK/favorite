from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars', default='/default/user.png')
    about_me = models.TextField(max_length=280)


class Interest(models.Model):
    user_interested = models.ManyToManyField(User, through='interested')
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

    def __str__(self):
        return f'({self.interest_type}) {self.name}'


class Interested(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    super_like = models.BooleanField(default=False)
    note = models.TextField(null=True, blank=True)

