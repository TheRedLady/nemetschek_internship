from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Tag(models.Model):
    tag_name = models.CharField(max_length=15)

    def __str__(self):
        return self.tag_name


class Post(models.Model):
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    tag = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.content


