from django.contrib import admin
from .models import Products, Review, Contact_us
# Register your models here.
admin.site.register(Products)
admin.site.register(Review)
admin.site.register(Contact_us)
