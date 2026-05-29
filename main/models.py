from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"

    def __str__(self):
        return f'دسته بندی : {self.name}'
    
class Brand(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=10000, blank=True)

    class Meta:
        verbose_name = "برند"
        verbose_name_plural = "برند ها"

    def __str__(self):
        return f'{self.name} : برند'
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    description = models.TextField(max_length=10000, blank=True)
    extra_info = models.TextField(max_length=10000, blank=True)
    picture = models.ImageField(upload_to='upload/products/')
    price = models.DecimalField(default=0, decimal_places=0, max_digits=12)
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=0, max_digits=12)

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

    def __str__(self):
        return f'محصول : {self.name}'
    
class PharmacyInfo(models.Model):
    #About Pharmacy :
    about_pharmacy = models.TextField(max_length=10000, blank=True)
    #Pharmacy's doctor :
    doctor_fullname = models.CharField(max_length=100)
    doctor_info = models.TextField(max_length=10000)
    #Pharmacy's phone numbers :
    pharmacy_phone1 = models.CharField(max_length=25) 
    pharmacy_phone2 = models.CharField(max_length=25)
    pharmacy_phone3 = models.CharField(max_length=25)
    #Pharmacy's Emails :
    pharmacy_email1 = models.EmailField(max_length=100) 
    pharmacy_email2 = models.EmailField(max_length=100)
    pharmacy_email3 = models.EmailField(max_length=100)
    #Pharmacy's Address :
    pharmacy_address = models.TextField(max_length=10000)

    class Meta:
        verbose_name = "مشخصات داروخانه"
        verbose_name_plural = "مشخصات داروخانه"

    def __str__(self):
        return f'مشخصات داروخانه'
    
class CustomerDeliveryInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    full_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=25, blank=True)
    address = models.TextField(max_length=500, blank=True)
    city = models.CharField(max_length=100, blank=True)
    province = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    #Customer's shopping cart saving info : ( Example : {'2':5,'1':3,...} )
    shopping_cart = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        verbose_name = "مشخصات ارسال سفارش مشتری"
        verbose_name_plural = "مشخضات ارسال سفارش مشتریان"

    def __str__(self):
        return f'مشخصات ارسال سفارش برای - {self.user}'
    
#Signal :  
@receiver(post_save, sender=User)
def create_delivery_info(sender, instance, created, **kwargs):
    if created:
        CustomerDeliveryInfo.objects.create(user=instance)

