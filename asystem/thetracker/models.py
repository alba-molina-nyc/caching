from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

#product
class Job(models.Model):
    order_num = models.CharField(max_length=275)
    SKU = models.CharField(max_length=275)
    description_text = models.TextField()
    num_items = models.IntegerField()
    num_stones = models.IntegerField()
    creator_name = models.ForeignKey(User, on_delete=models.PROTECT)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.order_num + ' | ' + str(self.creator_name) + ' | ' + str(self.created)
    
    def get_absolute_url(self):
        return reverse('add-job')

    @property
    def calculate_total_amt(self):
        amt = 0.50
        num_stones = self.num_stones * amt
        return num_stones
   
#cart
class Memo(models.Model):
    memo_id = models.CharField(max_length=250, blank=True)
    date_set = models.DateField(auto_now_add=True)
   
    
    def __str__(self):
        return self.memo_id

#cartitem
class MemoItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    memo = models.ForeignKey(Memo, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)
    quantity = models.IntegerField()

    def sub_total(self):
        return self.job.num_stones * 0.50


# create order model
class Order(models.Model):
    STATUS = (
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    order_number = models.CharField(max_length=20, default=None)
    setter_fname = models.CharField(max_length=250, blank=True)
    setter_lname = models.CharField(max_length=250, blank=True)
    setter_email = models.EmailField(max_length=50)
    note = models.CharField(max_length=100, blank=True)
    order_total = models.FloatField()
    is_memoed = models.BooleanField(default=False) #only has been assigned when setter receives it
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    created_at = models.DateTimeField(auto_now_add=True)
    creator_name = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)



    

   


   

 