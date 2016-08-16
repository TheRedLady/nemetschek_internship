from django.contrib import admin


from .models import Post, Tag


# Register your models here.


class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Content', {'fields':['content']}),
        ('Tags', {'fields': ['tag']})
    ]
    list_display = ('content', 'pub_date', 'last_modified')
    filter_horizontal = ('tag',)


admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
