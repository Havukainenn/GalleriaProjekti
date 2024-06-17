from django.contrib import admin
from .models import Folder, Image
from django.utils.html import format_html


#To-do : fix image page to be more coherent and organized / actually use the thumbnails

class FolderAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created', 'modified')
    list_filter = ('user', 'created')
    search_fields = ('name', 'user__username', 'user__email')
    ordering = ('-created',)

class ImageAdmin(admin.ModelAdmin):
    list_display = ('display_image', 'description', 'folder', 'user', 'created', 'modified')
    list_filter = ('folder__user', 'folder', 'created')
    search_fields = ('description', 'folder__name', 'folder__user__username', 'folder__user__email')
    ordering = ('-created',)

    def display_image(self, obj):
        if obj.file:
            return format_html('<img src="{}" width="150" height="150"/>', obj.file.url)
        return "No Image"
    display_image.short_description = 'Image'

admin.site.register(Folder, FolderAdmin)
admin.site.register(Image, ImageAdmin)
