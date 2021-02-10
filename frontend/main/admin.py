from .models import Repository
from .models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


admin.site.register(User, UserAdmin)

class RepositoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(Repository, RepositoryAdmin)
