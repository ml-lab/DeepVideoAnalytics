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


class Frame(models.Model):
    video = models.ForeignKey(Video,null=True)
    time_seconds = models.IntegerField()
    name = models.CharField(max_length=200,null=True)


class Query(models.Model):
    created = models.DateTimeField('date created', auto_now_add=True)
    results = models.BooleanField(default=False)
    task_id = models.CharField(max_length=100,default="")
    results_metadata = models.TextField(default="")

class Detection(models.Model):
    video = models.ForeignKey(Video,null=True)
    frame = models.ForeignKey(Frame)
    object_name = models.CharField(max_length=100)
    confidence = models.FloatField(default=0.0)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    h = models.IntegerField(default=0)
    w = models.IntegerField(default=0)
    metadata = models.TextField(default="")


class IndexEntries(models.Model):
    video = models.ForeignKey(Video,null=True)
    framelist = models.CharField(max_length=100)
    algorithm = models.CharField(max_length=100)
    count = models.IntegerField()

class TEvent(models.Model):
    started = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    video = models.ForeignKey(Video,null=True)
    operation = models.CharField(max_length=100,default="")
    recorded = models.DateTimeField('date created', auto_now_add=True)


class QueryResults(models.Model):
    query = models.ForeignKey(Query)
    video = models.ForeignKey(Video)
    frame = models.ForeignKey(Frame)
    algorithm = models.CharField(max_length=100)
    distance = models.FloatField(default=0.0)