from django.db import models


class Brand(models.Model):
    brd_id = models.IntegerField(primary_key=True)
    brd_name = models.CharField(max_length=20, blank=True, null=True)
    objects = models.Manager()

    class Meta:
        managed = True
        db_table = 'brand'


class Common(models.Model):
    com_id = models.IntegerField(primary_key=True)
    brd = models.ForeignKey(Brand, models.DO_NOTHING, blank=True, null=True)
    com_name = models.CharField(max_length=100, blank=True, null=True)
    com_img = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'common'

class Product(models.Model):
    prd_id = models.AutoField(primary_key=True)
    shop = models.ForeignKey('Shop', models.DO_NOTHING, blank=True, null=True)
    com = models.ForeignKey(Common, models.DO_NOTHING, blank=True, null=True)
    prd_name_shop = models.CharField(max_length=200, blank=True, null=True)
    prd_url = models.CharField(max_length=1000, blank=True, null=True)
    prd_desc = models.CharField(max_length=2000, blank=True, null=True)
    prd_price = models.CharField(max_length=20, blank=True, null=True)
    prd_discount = models.CharField(max_length=100, blank=True, null=True)
    prd_shipping = models.CharField(max_length=100, blank=True, null=True)
    prd_benefit = models.CharField(max_length=100, blank=True, null=True)
    prd_gift = models.CharField(max_length=100, blank=True, null=True)
    rev_avg = models.FloatField(blank=True, null=True)
    rev_cnt = models.IntegerField(blank=True, null=True)


    class Meta:
        managed = True
        db_table = 'product'

class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    prd = models.ForeignKey(Product, models.DO_NOTHING, blank=True, null=True)
    review_rating = models.FloatField(blank=True, null=True)
    review_title = models.CharField(max_length=100, blank=True, null=True)
    review_text = models.CharField(max_length=2000, blank=True, null=True)
    review_date = models.CharField(max_length=30, blank=True, null=True)
    review_userid = models.CharField(max_length=20, blank=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return self.name
    class Meta:
        managed = True
        db_table = 'review'


class Shop(models.Model):
    shop_id = models.IntegerField(primary_key=True)
    shop_name = models.CharField(max_length=20, blank=True, null=True)
    
    objects = models.Manager()

    def __str__(self):
        return self.name
    class Meta:
        managed = True
        db_table = 'shop'