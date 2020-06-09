from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class Buyer(models.Model):
    first_name = models.CharField(max_length=100)
    id_number = models.IntegerField(null=False,unique=True)
    occupation = models.CharField(max_length=100)
    phone_number=models.IntegerField()
    email = models.CharField(max_length=100)
    kra_pin = models.CharField(max_length=100)
    profile=models.ImageField(upload_to='profile', default='profile/default.jpg',blank=False)
    kin_name = models.CharField(max_length=100)
    kin_phone_number = models.IntegerField()
    created_date = models.DateTimeField(default=timezone.now)
    #updated_date = models.DateTimeField(default=timezone.now)
    created_user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    #updated_user = models.CharField(max_length=100)
    #slug = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name}-{self.id_number} Buyer'
    
    @property
    def items(self):
        return self.item_set.all()

class Item(models.Model):
    buyer=models.ForeignKey(Buyer,on_delete=models.CASCADE)
    make=models.CharField(max_length=50)
    model=models.CharField(max_length=50)
    colour=models.CharField(max_length=50)
    year=models.IntegerField()
    reg_number=models.CharField(max_length=50)
    engine_number=models.CharField(max_length=100)
    chassis_number=models.CharField(max_length=100)
    odometer_reading=models.CharField(max_length=100)
    regitered_car_owner=models.CharField(max_length=100)
    price=models.IntegerField(blank=False)

    def __str__(self):
        return f'{self.buyer.first_name}-{self.reg_number} Item'

    @property
    def agreement(self):
        return self.agreement_set.all()

class Agreement(models.Model):
    date_created=models.DateField(default=timezone.now)
    buyer=models.ForeignKey(Buyer,on_delete=models.CASCADE)
    item=models.OneToOneField(Item,on_delete=models.CASCADE)
    buyer_signature=models.ImageField(upload_to='signatures',default='default.jpg')
    witness_one_name=models.CharField(max_length=50,default='**')
    witness_one_signature=models.ImageField(upload_to='signatures/witness',default='default.jpg')
    witness_one_id_number=models.IntegerField(default=11)
    witness_one_phone_number=models.IntegerField(default=11)
    witness_one_email=models.CharField(max_length=50,default='**')
    witness_two_name=models.CharField(max_length=50,default='**')
    witness_two_signature=models.ImageField(upload_to='signatures/witness,',default='default.jpg')
    witness_two_id_number=models.IntegerField(default=11)
    witness_two_phone_number=models.IntegerField(default=11)
    witness_two_email=models.CharField(max_length=50,default='**')

    def __str__(self):
        return f'{self.buyer.first_name}-{self.item.reg_number} Agreement'
        

