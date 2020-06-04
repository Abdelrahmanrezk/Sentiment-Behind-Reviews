from django.db import models
	
# Create your models here.


class Products(models.Model):
	product_title  = models.CharField(max_length=1000, verbose_name=u"Product_title",null=False, blank=False)
	product_url = models.URLField(null=False, blank=False)
	image_src = models.URLField(null=False, blank=False)
	product_new_price = models.FloatField(null=True, blank=False)
	product_old_price = models.FloatField(null=True, blank=True, default=0.0)
	product_discount_percentage = models.FloatField(null=True, blank=True, default=0.0)
	product_discount_value = models.FloatField(null=True, blank=True, default=0.0)
	
	class Meta:
		db_table = "products"



class Review(models.Model):
	review = models.ForeignKey(Products, related_name='product_review', on_delete=models.CASCADE,)
	product_review = models.CharField(max_length=1000)



class Contact_us(models.Model):
    first_name = models.CharField(max_length=50)
    mail = models.EmailField()
    phonenumber = models.CharField(max_length=50)
    message = models.CharField(max_length=2000)

    class Meta:
    	verbose_name_plural = "contact_us"
    	db_table = "contact_us"

