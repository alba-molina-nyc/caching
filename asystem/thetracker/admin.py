from django.contrib import admin
from .models import Job, Memo, MemoItem, Order

admin.site.register(Job)
admin.site.register(Memo)
admin.site.register(MemoItem)
admin.site.register(Order)