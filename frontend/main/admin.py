from .models import Repository
from .models import AuthorizedKey
from django.contrib import admin

# from .models import User
# from django.contrib.auth.admin import UserAdmin
# admin.site.register(User, UserAdmin)

class RepositoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(Repository, RepositoryAdmin)


class AuthorizedKeyAdmin(admin.ModelAdmin):
    pass
admin.site.register(AuthorizedKey, AuthorizedKeyAdmin)
