from django.db import models


class Status(models.TextChoices):
    active = '#1', 'active'
    done = '#2', 'done'
    freeze = '#3', 'freeze'
