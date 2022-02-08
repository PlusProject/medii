from django.db import models

# Create your models here.


class ClinicalTrials(models.Model):
    cid = models.AutoField(primary_key=True)
    source_name = models.CharField(max_length=255, blank=True, null=True)
    source_id = models.IntegerField(blank=True, null=True)
    chief_name = models.CharField(max_length=255, blank=True, null=True)
    title_kor = models.CharField(max_length=2000, blank=True, null=True)
    title_eng = models.TextField(blank=True, null=True)
    recruitment_state = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.CharField(max_length=255, blank=True, null=True)
    end_date = models.CharField(max_length=255, blank=True, null=True)
    disease_code = models.TextField(blank=True, null=True)
    disease_detail = models.CharField(max_length=2000, blank=True, null=True)
    rare_disease = models.IntegerField(blank=True, null=True)
    url = models.CharField(max_length=1000, blank=True, null=True)

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
    pid = models.OneToOneField(
        Person, models.DO_NOTHING, db_column='pid', primary_key=True, related_name='doctor')
    education = models.TextField(blank=True, null=True)
    career = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'doctor'


class Participate(models.Model):
    pcid = models.AutoField(primary_key=True)
    pid = models.ForeignKey(Person, models.DO_NOTHING,
                            db_column='pid', related_name='participate')
    cid = models.ForeignKey(ClinicalTrials, models.DO_NOTHING,
                            db_column='cid', related_name='clinical_trials')
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
    pid = models.ForeignKey(Person, models.DO_NOTHING,
                            db_column='pid', related_name='writes')
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


class DoctorTotalDisease(models.Model):
    id = models.IntegerField(primary_key=True)
    name_kor = models.CharField(
        max_length=45, db_collation='utf8mb4_bin', blank=True, null=True)
    belong = models.CharField(
        max_length=45, db_collation='utf8mb4_bin', blank=True, null=True)
    major = models.TextField(db_collation='utf8mb4_bin', blank=True, null=True)
    paper_count = models.IntegerField(blank=True, null=True)
    paper_impact = models.FloatField(blank=True, null=True)
    paper_disease_all = models.TextField(
        db_collation='utf8mb4_bin', blank=True, null=True)
    clinical_count = models.IntegerField(blank=True, null=True)
    clinical_disease_all = models.TextField(
        db_collation='utf8mb4_bin', blank=True, null=True)
    img = models.TextField(db_collation='utf8mb4_bin', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'doctor_total_disease'


class Totaldisease(models.Model):
    id = models.IntegerField(primary_key=True)
    disease_code = models.TextField(blank=True, null=True)
    disease_kor = models.TextField(blank=True, null=True)
    disease_eng = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'totaldisease'


class DoctorAllscore(models.Model):
    belong_name = models.CharField(
        primary_key=True, max_length=255, db_collation='utf8_general_ci')
    disease = models.TextField(
        db_collation='utf8_general_ci', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'doctor_allscore'

#동완 네트워크
class SnPaper(models.Model):
    id = models.AutoField(primary_key=True)
    label = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    shape = models.TextField(blank=True, null=True)
    color = models.TextField(blank=True, null=True)
    size = models.FloatField(blank=True, null=True)
    borderWidth = models.IntegerField(blank=True, null=True)
    belong = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'SN_paper'

class SnPaperCnt(models.Model):
    id = models.IntegerField(primary_key=True)
    fromit = models.IntegerField(blank=True, null=True)
    toit = models.IntegerField(blank=True, null=True)
    width = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'SN_paper_cnt'

class NodeCris(models.Model):
    id = models.IntegerField(primary_key=True)
    label = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    shape = models.TextField(blank=True, null=True)
    color = models.TextField(blank=True, null=True)
    size = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'node_cris'


class NodeCrisCnt(models.Model):
    id = models.IntegerField(primary_key=True)
    fromit = models.IntegerField(blank=True, null=True)
    toit = models.IntegerField(blank=True, null=True)
    width = models.FloatField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'node_cris_cnt'


class SnPaper50(models.Model):
    id = models.AutoField(primary_key=True)
    label = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    shape = models.TextField(blank=True, null=True)
    color = models.TextField(blank=True, null=True)
    size = models.FloatField(blank=True, null=True)
    borderWidth = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'SN_paper50'


class SnPaperCnt50(models.Model):
    id = models.IntegerField(primary_key=True)
    fromit = models.IntegerField(blank=True, null=True)
    toit = models.IntegerField(blank=True, null=True)
    width = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'SN_paper_cnt50'
class PartPaperEdge(models.Model):
    id = models.IntegerField(primary_key=True)
    fromit = models.IntegerField(blank=True, null=True)
    toit = models.IntegerField(blank=True, null=True)
    width = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'part_paper_edge'


class PartPaperNode(models.Model):
    id = models.IntegerField(primary_key=True)
    label = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    shape = models.TextField(blank=True, null=True)
    color = models.TextField(blank=True, null=True)
    size = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'part_paper_node'

class SnPaperEdgeYear(models.Model):
    id = models.IntegerField(primary_key=True)
    fromit = models.IntegerField(blank=True, null=True)
    toit = models.IntegerField(blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    y2021 = models.IntegerField(blank=True, null=True)
    y2020 = models.IntegerField(blank=True, null=True)
    y2019 = models.IntegerField(blank=True, null=True)
    y2018 = models.IntegerField(blank=True, null=True)
    y2017 = models.IntegerField(blank=True, null=True)
    y2016 = models.IntegerField(blank=True, null=True)
    y2015 = models.IntegerField(blank=True, null=True)
    y2014 = models.IntegerField(blank=True, null=True)
    y2013 = models.IntegerField(blank=True, null=True)
    y2012 = models.IntegerField(blank=True, null=True)
    y2011 = models.IntegerField(blank=True, null=True)
    y2010 = models.IntegerField(blank=True, null=True)
    y2009 = models.IntegerField(blank=True, null=True)
    y2008 = models.IntegerField(blank=True, null=True)
    y2007 = models.IntegerField(blank=True, null=True)
    y2006 = models.IntegerField(blank=True, null=True)
    to2005 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'SN_paper_edge_year'
        
        
#acm 추천
class DoctorAll(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45, db_collation='utf8_general_ci', blank=True, null=True)
    belong = models.CharField(max_length=45, db_collation='utf8_general_ci', blank=True, null=True)
    disease = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    img = models.TextField(db_collation='utf8mb4_general_ci', blank=True, null=True)
    name_kor = models.CharField(max_length=45, db_collation='utf8mb4_bin', blank=True, null=True)
    belong2 = models.CharField(max_length=45, db_collation='utf8mb4_bin', blank=True, null=True)
    major = models.TextField(db_collation='utf8mb4_bin', blank=True, null=True)
    paper_count = models.IntegerField(blank=True, null=True)
    paper_disease_all = models.TextField(db_collation='utf8mb4_bin', blank=True, null=True)
    clinical_count = models.IntegerField(blank=True, null=True)
    clinical_disease_all = models.TextField(db_collation='utf8mb4_bin', blank=True, null=True)
    paper_impact = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'doctor_all'
        
class DoctorAll2(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45, db_collation='utf8_general_ci', blank=True, null=True)
    belong = models.CharField(max_length=45, db_collation='utf8_general_ci', blank=True, null=True)
    disease = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    img = models.TextField(db_collation='utf8mb4_general_ci', blank=True, null=True)
    name_kor = models.CharField(max_length=45, db_collation='utf8mb4_bin', blank=True, null=True)
    belong2 = models.CharField(max_length=45, db_collation='utf8mb4_bin', blank=True, null=True)
    major = models.TextField(db_collation='utf8mb4_bin', blank=True, null=True)
    paper_count = models.IntegerField(blank=True, null=True)
    paper_disease_all = models.TextField(db_collation='utf8mb4_bin', blank=True, null=True)
    clinical_count = models.IntegerField(blank=True, null=True)
    clinical_disease_all = models.TextField(db_collation='utf8mb4_bin', blank=True, null=True)
    paper_impact = models.FloatField(blank=True, null=True)
    a = models.TextField(db_column='A', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    b = models.TextField(db_column='B', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    c = models.TextField(db_column='C', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    d = models.TextField(db_column='D', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    e = models.TextField(db_column='E', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    f = models.TextField(db_column='F', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    g = models.TextField(db_column='G', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    h = models.TextField(db_column='H', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    i = models.TextField(db_column='I', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    j = models.TextField(db_column='J', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    k = models.TextField(db_column='K', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    l = models.TextField(db_column='L', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    m = models.TextField(db_column='M', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    n = models.TextField(db_column='N', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    o = models.TextField(db_column='O', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    p = models.TextField(db_column='P', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    q = models.TextField(db_column='Q', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    r = models.TextField(db_column='R', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    s = models.TextField(db_column='S', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    t = models.TextField(db_column='T', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    u = models.TextField(db_column='U', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    v = models.TextField(db_column='V', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    w = models.TextField(db_column='W', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    x = models.TextField(db_column='X', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    y = models.TextField(db_column='Y', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    z = models.TextField(db_column='Z', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'doctor_all2'

class DoctorAll3(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name_kor = models.CharField(max_length=45, db_collation='utf8_general_ci', blank=True, null=True)
    belong = models.CharField(max_length=45, db_collation='utf8_general_ci', blank=True, null=True)
    major = models.TextField(db_collation='utf8mb4_general_ci', blank=True, null=True)
    education = models.TextField(db_collation='utf8mb4_general_ci', blank=True, null=True)
    career = models.TextField(db_collation='utf8mb4_general_ci', blank=True, null=True)
    img = models.TextField(db_collation='utf8mb4_general_ci', blank=True, null=True)
    link = models.TextField(db_collation='utf8mb4_general_ci', blank=True, null=True)
    hospital_code = models.TextField(db_collation='utf8mb4_general_ci', blank=True, null=True)
    disease = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    a = models.TextField(db_column='A', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    b = models.TextField(db_column='B', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    c = models.TextField(db_column='C', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    d = models.TextField(db_column='D', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    e = models.TextField(db_column='E', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    f = models.TextField(db_column='F', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    g = models.TextField(db_column='G', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    h = models.TextField(db_column='H', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    i = models.TextField(db_column='I', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    j = models.TextField(db_column='J', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    k = models.TextField(db_column='K', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    l = models.TextField(db_column='L', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    m = models.TextField(db_column='M', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    n = models.TextField(db_column='N', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    o = models.TextField(db_column='O', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    p = models.TextField(db_column='P', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    q = models.TextField(db_column='Q', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    r = models.TextField(db_column='R', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    s = models.TextField(db_column='S', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    t = models.TextField(db_column='T', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    u = models.TextField(db_column='U', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    v = models.TextField(db_column='V', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    w = models.TextField(db_column='W', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    x = models.TextField(db_column='X', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    y = models.TextField(db_column='Y', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    z = models.TextField(db_column='Z', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    paper_count = models.IntegerField(blank=True, null=True)
    paper_impact = models.FloatField(blank=True, null=True)
    clinical_count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'doctor_all3'