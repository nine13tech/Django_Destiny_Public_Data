from django.db import models


class Milestones(models.Model):
    hash_id = models.IntegerField(blank=True, null=True)
    event_type = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    icon = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    has_variant = models.BooleanField(blank=False, null=False, default=0)

    class Meta:
        managed = True
        db_table = 'dpd_milestones'


class Variants(models.Model):
    """ Contains both Variants and Challenges """
    parent_hash_id = models.IntegerField(blank=True, null=True)
    modifier_type = models.TextField(blank=True, null=True)
    hash_id = models.IntegerField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    icon = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'dpd_variants'
