from blog.models import Tag, Category, Page, Post
from django.contrib import admin


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display: tuple = ('id', 'name', 'slug')
    list_display_links: tuple = ('name',)
    search_fields: tuple = ('id', 'name', 'slug')
    list_per_page: int = 10
    ordering: tuple = ('-id',)
    prepopulated_fields: dict = {'slug': ('name',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display: tuple = ('id', 'name', 'slug')
    list_display_links: tuple = ('name',)
    search_fields: tuple = ('id', 'name', 'slug')
    list_per_page: int = 10
    ordering: tuple = ('-id',)
    prepopulated_fields: dict = {'slug': ('name',)}


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display: tuple = ('id', 'title', 'is_published')
    list_display_links: tuple = ('title',)
    search_fields: tuple = ('id', 'slug', 'title', 'content')
    list_per_page: int = 50
    list_filter: tuple = ('is_published',)
    list_editable: tuple = ('is_published',)
    ordering: tuple = ('-id',)
    prepopulated_fields: dict = {'slug': ('title',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display: tuple = ('id', 'title', 'is_published', 'created_at')
    list_display_links: tuple = ('title',)
    search_fields: tuple = ('id', 'slug', 'title', 'excerpt', 'content')
    list_per_page: int = 50
    list_filter: tuple = ('category', 'is_published')
    list_editable: tuple = ('is_published',)
    ordering: tuple = ('-id',)
    readonly_fields: tuple = (
        'created_at', 'updated_at', 'created_by', 'updated_by'
    )
    prepopulated_fields: dict = {'slug': ('title',)}
    autocomplete_fields: tuple = ('category', 'tags')

    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user
        else:
            obj.created_by = request.user
        obj.save()
