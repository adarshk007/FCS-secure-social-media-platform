from django.db import models
from account.models import Account
from django.db.models import Q
from django.utils import timezone

# Create your models here.

class Friend(models.Model):
	user_1 = models.ForeignKey(Account, related_name="user_1", null=True, on_delete=models.CASCADE)
	user_2 = models.ForeignKey(Account, related_name="user_2", null=True, on_delete=models.CASCADE)
	status = models.BooleanField(default=False)
	date_requested = models.DateTimeField(verbose_name="date requested", auto_now_add=True)
	date_confirmed = models.DateTimeField(verbose_name="date confirmed", null=True)


class Wallet(models.Model):
	user = models.ForeignKey(Account, related_name="user", on_delete=models.CASCADE)
	balance = models.IntegerField(default = 0)

class Transaction(models.Model):
	user_1 = models.ForeignKey(Account, related_name="t_user_1", null=True, on_delete=models.CASCADE)
	user_2 = models.ForeignKey(Account, related_name="t_user_2", null=True, on_delete=models.CASCADE)
	amount = models.FloatField(default = 0)
	payment_method = models.TextField(default = 'paytm')
	status = models.BooleanField(default=False)
	date_requested = models.DateTimeField(verbose_name="date requested", auto_now_add=True)
	date_confirmed = models.DateTimeField(verbose_name="date confirmed", null=True)
	
class feed(models.Model):

    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    post_to = models.ForeignKey(Account, on_delete=models.SET_NULL,null=True,related_name="other_users")
    content = models.TextField(null=False)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.author.first_name

class Message(models.Model):
	user_1 = models.ForeignKey(Account, related_name="user_send", null=True, on_delete=models.CASCADE)
	user_2 = models.ForeignKey(Account, related_name="user_recv", null=True, on_delete=models.CASCADE)    
	message = models.TextField(verbose_name="message")
	message_sent = models.DateTimeField(verbose_name="message_sent", auto_now_add=True)

class Page(models.Model):
	user = models.ForeignKey(Account, related_name="page_create_user", null=True, on_delete=models.CASCADE) 
	page_title = models.TextField(null= False)
	content = models.TextField(null=False)
	date_created = models.DateTimeField(verbose_name="date created", auto_now_add=True)
