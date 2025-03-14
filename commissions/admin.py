from django.contrib import admin
from .models import Commission, Comment


class CommentInline(admin.TabularInline):
    """
    Inline editing of comments in the Commission admin page.
    """
    model = Comment
    extra = 1  # Show one empty inline form as a default for new comments.
    readonly_fields = ("created_on", "updated_on") 


class CommissionAdmin(admin.ModelAdmin):
    """
    Admin customization for Commission model.
    """
    model = Commission
    list_display = (
        "title", 
        "people_required", 
        "created_on", 
        "updated_on"
    ) 
    search_fields = ("title", "description")  
    list_filter = ("created_on", "updated_on") 
    inlines = [CommentInline] 


class CommentAdmin(admin.ModelAdmin):
    """
    Admin customization for Comment model.
    """
    model = Comment
    list_display = ("commission", "entry", "created_on", "updated_on") 
    search_fields = ("commission__title", "entry") 
    list_filter = ("created_on", "updated_on", "commission") 


# Register models.
admin.site.register(Commission, CommissionAdmin)
admin.site.register(Comment, CommentAdmin)