from gallery.models import Project, Picture, Style
from django.contrib import admin

class PictureInline(admin.StackedInline):
    model = Picture
    extra = 2
    fieldsets = [
        ('Upload',       {'fields': ['image', 'title', 'picture_type']}),
    ]

class ProjectAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Name',       {'fields': ['project']}),
        ('Information', {'fields': ['banner']}),#, 'pub_date']}),
    ]
    #readonly_fields=('banner','pub_date')
    inlines = [PictureInline]
    list_display = ('project','pub_date')
    list_filter = ['pub_date']
    search_fields = ['question']
    date_hierarchy = 'pub_date'

class StyleAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Style',       {'fields': [
            'bg_color', ('banner_width', 'banner_height'), 
            ('thumbs_per_row', 'thumbs_per_page'), 
            ('image_width', 'image_height')]}),
        ('Information', {'fields': [('thumb_width', 'thumb_height')]}),
    ]
    readonly_fields=('thumb_width', 'thumb_height')

admin.site.register(Project, ProjectAdmin)
admin.site.register(Picture)
admin.site.register(Style, StyleAdmin)