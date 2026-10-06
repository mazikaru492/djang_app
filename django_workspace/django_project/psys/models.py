from django.db import models


class Customer(models.Model):
    customer_code = models.CharField(max_length=6, primary_key=True)
    customer_name = models.CharField(max_length=32, blank=True, null=True)
    customer_telno = models.CharField(max_length=13, blank=True, null=True)
    customer_postalcode = models.CharField(max_length=8, blank=True, null=True)
    customer_address = models.CharField(max_length=40, blank=True, null=True)
    discount_rate = models.IntegerField(blank=True, null=True)
    delete_flag = models.IntegerField()

    class Meta:
        db_table = 'customer'
        managed = True
