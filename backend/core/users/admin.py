from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(User)
admin.site.register(Publisher)
admin.site.register(Commenter)
admin.site.register(Followers)
admin.site.register(SecretKeys)

