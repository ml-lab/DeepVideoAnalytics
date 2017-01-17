from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Video(models.Model):
    bucket = models.CharField(max_length=100,default="")
    key = models.CharField(max_length=100,default="")
    name = models.CharField(max_length=100,default="")
    length_in_seconds = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    width = models.IntegerField(default=0)
    metadata = models.TextField(default="")
    frames = models.IntegerField(default=0)
    created = models.DateTimeField('date created', auto_now_add=True)
    description = models.TextField(default="")
    uploaded = models.BooleanField(default=False)

class Dataset(models.Model):
    bucket = models.CharField(max_length=100)
    key = models.CharField(max_length=100)
    metadata = models.TextField(default="")
    frames = models.IntegerField()
    created = models.DateTimeField('date created', auto_now_add=True)
    description = models.TextField()

class Frame(models.Model):
    video = models.ForeignKey(Video,null=True)
    dataset = models.ForeignKey(Dataset,null=True)
    time_seconds = models.IntegerField()
    key = models.CharField(max_length=200)
    bucket = models.CharField(max_length=200)

class Detection(models.Model):
    video = models.ForeignKey(Video,null=True)
    dataset = models.ForeignKey(Dataset,null=True)
    frame = models.ForeignKey(Frame)
    object_name = models.CharField(max_length=100)
    confidence = models.FloatField(default=0.0)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    h = models.IntegerField(default=0)
    w = models.IntegerField(default=0)


class IndexEntry(models.Model):
    video = models.ForeignKey(Video,null=True)
    dataset = models.ForeignKey(Dataset,null=True)
    detection = models.ForeignKey(Detection,null=True)
    frame = models.ForeignKey(Frame)
    algorithm = models.CharField(max_length=100)
    d = models.IntegerField(default=0)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    h = models.IntegerField(default=0)
    w = models.IntegerField(default=0)
    array_index = models.IntegerField()

class TEvent(models.Model):
    started = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    dataset = models.ForeignKey(Dataset,null=True)
    video = models.ForeignKey(Video,null=True)
    frame = models.ForeignKey(Frame,null=True)
    recorded = models.DateTimeField('date created', auto_now_add=True)
