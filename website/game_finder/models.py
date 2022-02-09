from django.db import models
from urllib.parse import urlparse


class Game(models.Model):
    name = models.CharField(max_length=250)
    price = models.IntegerField(default=0)
    status = models.BooleanField(default=0)
    link = models.CharField(max_length=350)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']

    def get_shop_name(self):
        name = urlparse(self.link).hostname
        if name == 'www.drustveneigre.rs':
            name = 'mipl.rs'
            return name
        else:
            return name