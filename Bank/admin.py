from django.contrib import admin
from Bank import models


admin.site.register(models.Account)
admin.site.register(models.Balance)
admin.site.register(models.ActionsRegister)
admin.site.register(models.Feedback)
