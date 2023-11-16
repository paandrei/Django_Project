from django.db import models
import os 
from currency_converter import views as w 

class Account(models.Model):

    username = models.CharField(primary_key=True, max_length=100) 
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.IntegerField()
    email = models.EmailField()
    phone = models.IntegerField()
    password = models.CharField(default=None, max_length=100)
    currency = models.CharField(default=None, max_length=3)
    iban = models.CharField(default=None, max_length=14)

    class Meta:
        db_table = 'accounts'

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

class Balance(models.Model):
    iban = models.CharField(primary_key=True, max_length=14, default=None)
    username = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    balance = models.FloatField(default=0.00)
    class Meta:
        db_table = 'Balances'

    def __str__(self) -> str:
        return f'{self.username.first_name} {self.balance} {self.username.currency}'
    

class Feedback(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    name = models.CharField(default=None, max_length=100)
    email = models.EmailField(default=None)
    subject = models.CharField(default=None, max_length=150)
    the_request = models.TextField(default=None, max_length=1000)

    class Meta:
        db_table = 'Feedback'

    def __str__(self):
        return f'{self.name}    {self.subject}'
    
class ActionsRegister(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    username = models.ForeignKey(Account, blank=True, on_delete=models.CASCADE, null= True)
    action_name = models.CharField(default='', max_length=50)
    date = models.DateField(default=None)
    amount = models.FloatField(default=0.0)
    class Meta:
        db_table = f'Register'

    def __str__(self):
        return f'{self.username.first_name} {self.username.last_name} {self.action_name}'


    