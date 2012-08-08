from gallery.models import Project, Picture
from django.contrib import admin

class PictureInline(admin.StackedInline):
    model = Picture
    extra = 3
    fieldsets = [
        ('Upload',       {'fields': ['image', 'picture_type', 'title']}),
    ]

class ProjectAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Name',       {'fields': ['project']}),
        ('Information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [PictureInline]
    list_display = ('project','pub_date')
    list_filter = ['pub_date']
    search_fields = ['question']
    date_hierarchy = 'pub_date'

admin.site.register(Project, ProjectAdmin)
admin.site.register(Picture)