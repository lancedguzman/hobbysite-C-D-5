from django.contrib import admin
from .models import post, post_category

class post_admin(admin.ModelAdmin):
    model = post
    
    list_display = ('title', 'category', 'created_on', 'updated_on')

class post_category_admin(admin.ModelAdmin):
    model = post_category

    list_display = ('name',)


admin.site.register(post, post_admin)
admin.site.register(post_category, post_category_admin)

