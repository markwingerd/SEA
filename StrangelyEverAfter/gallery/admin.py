from gallery.models import Project, GalleryImage
from django.contrib import admin

class GalleryImageInline(admin.StackedInline):
    model = GalleryImage
    extra = 1

class ProjectAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Name',       {'fields': ['project']}),
        ('Information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [GalleryImageInline]
    list_display = ('project','pub_date')
    list_filter = ['pub_date']
    search_fields = ['question']
    date_hierarchy = 'pub_date'

admin.site.register(Project, ProjectAdmin)