import json

from django.db import models
from django.db.models.fields.json import KeyTransform


class JSONFieldJSONType(models.JSONField):
    """
    Custom JSON field because our postgres uses json type and not jsonb.

    Details on these changes within Django can be seen here:

    * https://code.djangoproject.com/ticket/31973
    * https://code.djangoproject.com/ticket/31956#comment:8

    PR that changed behavior for regular json type:
    https://github.com/django/django/commit/0be51d2226fce030ac9ca840535a524f41e9832c

    """

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        # Some backends (SQLite at least) extract non-string values in their
        # SQL datatypes.
        if isinstance(expression, KeyTransform) and not isinstance(value, str):
            return value
        try:
            # Custom implementation for how our data comes out of our postgres
            # connection.
            if isinstance(value, dict):
                data_value = self.get_prep_value(value)
            else:
                data_value = value
            return json.loads(data_value, cls=self.decoder)
        except json.JSONDecodeError:
            return value


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
    scraper_config = JSONFieldJSONType(default=dict, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    scraper = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'theater'
