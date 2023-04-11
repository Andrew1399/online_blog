from django.contrib import admin
from users.models import Reader, Author, Profile, Follow
# Register your models here.


class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author')
    search_fields = ('user', 'author')
    empty_value_display = '-empty'

admin.site.register(Reader)
admin.site.register(Author)
admin.site.register(Profile)
admin.site.register(Follow, FollowAdmin)