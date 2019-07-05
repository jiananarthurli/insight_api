from django.db import models

# Create your models here.


class EventList(models.Model):
    index = models.BigIntegerField(primary_key=True, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    link = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    venue = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'event_list'
