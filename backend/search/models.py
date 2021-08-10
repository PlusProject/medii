from django.db import models

# Create your models here.
class ClinicalTrials(models.Model):
    cid = models.AutoField(primary_key=True)
    source_name = models.CharField(max_length=255, blank=True, null=True)
    source_id = models.IntegerField(blank=True, null=True)
    title_kor = models.CharField(max_length=255, blank=True, null=True)
    title_eng = models.TextField(blank=True, null=True)
    recruitment_state = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.CharField(max_length=255, blank=True, null=True)
    end_date = models.CharField(max_length=255, blank=True, null=True)
    disease = models.TextField(blank=True, null=True)
    disease_detail = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clinical_trials'


class Person(models.Model):
    pid = models.AutoField(primary_key=True)
    name_kor = models.CharField(max_length=255, blank=True, null=True)
    belong = models.CharField(max_length=255, blank=True, null=True)
    job = models.CharField(max_length=255, blank=True, null=True)
    major = models.TextField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'person'


class Doctor(models.Model):
    pid = models.OneToOneField(Person, models.DO_NOTHING, db_column='pid', primary_key=True, related_name='doctor')
    education = models.TextField(blank=True, null=True)
    career = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'doctor'


class Participate(models.Model):
    pcid = models.AutoField(primary_key=True)
    pid = models.ForeignKey(Person, models.DO_NOTHING, db_column='pid', related_name='participate')
    cid = models.ForeignKey(ClinicalTrials, models.DO_NOTHING, db_column='cid')
    position = models.CharField(max_length=255, blank=True, null=True)
    source_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'participate'


class Thesis(models.Model):
    tid = models.AutoField(primary_key=True)
    name_kor = models.CharField(max_length=255, blank=True, null=True)
    belong = models.CharField(max_length=255, blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    journal = models.TextField(blank=True, null=True)
    publication_date = models.CharField(max_length=255, blank=True, null=True)
    citation = models.CharField(max_length=255, blank=True, null=True)
    coworker = models.TextField(blank=True, null=True)
    journal_index = models.CharField(max_length=45, null=True)

    class Meta:
        managed = False
        db_table = 'thesis'


class Writes(models.Model):
    wid = models.AutoField(primary_key=True)
    pid = models.ForeignKey(Person, models.DO_NOTHING, db_column='pid', related_name='writes')
    tid = models.ForeignKey(Thesis, models.DO_NOTHING, db_column='tid')

    class Meta:
        managed = False
        db_table = 'writes'


class Disease(models.Model):
    code = models.CharField(max_length=255, blank=True, null=True)
    name_kor = models.CharField(max_length=1000, blank=True, null=True)
    name_eng = models.CharField(max_length=1000, blank=True, null=True)
    rare = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'disease'