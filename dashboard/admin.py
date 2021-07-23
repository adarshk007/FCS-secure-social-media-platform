from django.contrib import admin
from dashboard.models import Friend, Wallet, Transaction, feed, Message, Page

# Register your models here.
admin.site.register(Friend)
admin.site.register(Wallet)
admin.site.register(Transaction)
admin.site.register(feed)
admin.site.register(Message)
admin.site.register(Page)
