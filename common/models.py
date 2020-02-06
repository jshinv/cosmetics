from django.db import models

class Brand(models.Model):
    brd_id = models.IntegerField(primary_key=True)
    brd_name = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'BRAND'


class Common(models.Model):
    com_id = models.IntegerField(primary_key=True)
    brd = models.ForeignKey(Brand, models.DO_NOTHING, blank=True, null=True)
    com_name = models.CharField(max_length=20, blank=True, null=True)
    com_img = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'COMMON'


class Product(models.Model):
    prd_id = models.IntegerField(primary_key=True)
    shop = models.ForeignKey('Shop', models.DO_NOTHING, blank=True, null=True)
    prd_name_shop = models.CharField(max_length=50, blank=True, null=True)
    prd_url = models.CharField(max_length=100, blank=True, null=True)
    prd_desc = models.CharField(max_length=100, blank=True, null=True)
    prd_price = models.CharField(max_length=20, blank=True, null=True)
    prd_discount = models.CharField(max_length=20, blank=True, null=True)
    prd_shipping = models.CharField(max_length=20, blank=True, null=True)
    prd_benefit = models.CharField(max_length=100, blank=True, null=True)
    prd_gift = models.CharField(max_length=100, blank=True, null=True)
    rev_avg = models.CharField(max_length=20, blank=True, null=True)
    rev_cnt = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'PRODUCT'


class Review(models.Model):
    review_id = models.IntegerField(primary_key=True)
    prd = models.ForeignKey(Product, models.DO_NOTHING, blank=True, null=True)
    review_rating = models.FloatField(blank=True, null=True)
    review_title = models.CharField(max_length=100, blank=True, null=True)
    review_text = models.CharField(max_length=500, blank=True, null=True)
    review_date = models.CharField(max_length=30, blank=True, null=True)
    review_user_id = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'REVIEW'


class Shop(models.Model):
    shop_id = models.IntegerField(primary_key=True)
    shop_name = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'SHOP'
