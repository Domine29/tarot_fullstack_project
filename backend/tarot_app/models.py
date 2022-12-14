from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import JSONField
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class SiteUser(AbstractUser):
    email = models.EmailField(max_length = 100, unique = True)
    phone_code=models.IntegerField(blank=True,null=True)
    cell_phone_number=models.TextField(max_length=12,blank=True,null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class TarotCard(models.Model):
    name = models.TextField()
    number = models.IntegerField()
    arcana = models.TextField()
    suit = models.TextField()
    img = models.TextField()
    keywords = ArrayField(models.TextField(), default=list)
    meanings = JSONField(default=dict)
    questions_to_ask = ArrayField(models.TextField(), default=list)


class Spread(models.Model):
    user = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    type = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)


class CardInSpread(models.Model):
    spread = models.ForeignKey(Spread, on_delete=models.CASCADE)
    tarot_card = models.ForeignKey(TarotCard, on_delete=models.CASCADE)
    position = models.IntegerField()
    reverse = models.BooleanField()


class Note(models.Model):
    card_in_spread = models.ForeignKey(CardInSpread, on_delete=models.CASCADE)
    description = models.TextField()
    interpretation = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class OverallNote(models.Model):
    spread = models.ForeignKey(Spread, on_delete=models.CASCADE)
    content = models.TextField()

class DreamEntry1(models.Model):
    user = models.EmailField()
    date = models.DateField(auto_now_add=True)
    description = models.TextField()
    associations = models.TextField()
    inner_dynamics = models.TextField()
    interpretation = models.TextField()
    ritual = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
