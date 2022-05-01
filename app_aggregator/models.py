# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Fedmovie(models.Model):
    id = models.IntegerField(primary_key=True)
    cardnumber = models.CharField(db_column='cardNumber', max_length=20)  # Field name made lowercase.
    foreignname = models.CharField(db_column='foreignName', max_length=500, blank=True, null=True)  # Field name made lowercase.
    filmname = models.CharField(max_length=500)
    studio = models.CharField(max_length=500, blank=True, null=True)
    cryearofproduction = models.CharField(db_column='crYearOfProduction', max_length=128, blank=True, null=True)  # Field name made lowercase.
    director = models.CharField(max_length=500, blank=True, null=True)
    scriptauthor = models.CharField(db_column='scriptAuthor', max_length=500, blank=True, null=True)  # Field name made lowercase.
    composer = models.CharField(max_length=500, blank=True, null=True)
    durationminute = models.IntegerField(db_column='durationMinute', blank=True, null=True)  # Field name made lowercase.
    durationhour = models.IntegerField(db_column='durationHour', blank=True, null=True)  # Field name made lowercase.
    agecategory = models.CharField(db_column='ageCategory', max_length=128, blank=True, null=True)  # Field name made lowercase.
    annotation = models.TextField(blank=True, null=True)
    countryofproduction = models.CharField(db_column='countryOfProduction', max_length=300, blank=True, null=True)  # Field name made lowercase.
    agelimit = models.IntegerField(db_column='ageLimit', blank=True, null=True)  # Field name made lowercase.
    posterpath = models.CharField(db_column='posterPath', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'fedmovie'


class Session(models.Model):
    theater = models.ForeignKey('Theater', models.DO_NOTHING)
    movie = models.ForeignKey(Fedmovie, models.DO_NOTHING)
    hall = models.CharField(max_length=100, blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True)
    link = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'session'
        unique_together = (('theater', 'movie', 'hall', 'datetime'),)


class Theater(models.Model):
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=500, blank=True, null=True)
    scraper_config = models.JSONField(blank=True, null=True)  # This field type is a guess.
    city = models.CharField(max_length=200, blank=True, null=True)
    scraper = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'theater'
