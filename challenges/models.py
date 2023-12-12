import json
import datetime

from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=256)
    author_full_name = models.CharField(max_length=256)
    isbn = models.CharField(max_length=10)

    def __str__(self):
        return self.title


class Laptop(models.Model):
    brand = models.CharField(max_length=256)
    year_of_production = models.IntegerField()
    ram = models.CharField(max_length=64)
    hdd = models.CharField(max_length=64)
    price = models.FloatField()
    quantity = models.IntegerField()
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.brand + ' ' + self.ram + 'Gb RAM ' + self.hdd + 'Gb HDD'

    def to_json(self):
        return json.dumps({'brand': self.brand, 'year_of_production': self.year_of_production,
                           'ram': self.ram, 'hdd': self.hdd, 'price': self.price,
                           'quantity': self.quantity, 'date_added': self.date_added})


class Post(models.Model):
    title = models.CharField(max_length=256)
    text = models.CharField(max_length=16384, default='')
    author_name = models.CharField(max_length=256)
    status = models.CharField(choices=[('posted', 'Опубликован'),
                                       ('not_posted', 'Не опубликован'),
                                       ('banned', 'Забанен')],
                              default='not_posted',
                              max_length=256)
    date_created = models.DateTimeField(auto_now_add=True)
    date_posted = models.DateTimeField(auto_now=True)
    category = models.CharField(choices=[('fun', 'Funny posts'),
                                         ('news', 'News posts'),
                                         ('other', 'Any other topics')],
                                null=True,
                                max_length=256)

    def __str__(self):
        return self.title + ' by ' + self.author_name + ' created at ' \
            + self.date_created.strftime("%m/%d/%Y, %H:%M:%S") + ' ' + self.status

    def to_json(self):
        json_dict = {k: (v if type(v) != datetime.datetime
                         else v.strftime("%m/%d/%Y, %H:%M:%S"))
                     for k, v in vars(self).items() if k != '_state'}
        return json.dumps(json_dict)
