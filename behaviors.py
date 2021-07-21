from django.db import models
import time


class TimeStampable(models.Model):
  created_at = models.TextField(default=time.time())
  updated_at = models.TextField(blank=True)

  class Meta:
    abstract = True


class Deleteable(models.Model):
  deleted_at = models.BooleanField(default=False)

  class Meta:
    abstract = True


class Countable(models.Model):
  counted_at = models.IntegerField(default=0)

  class Meta:
    abstract = True