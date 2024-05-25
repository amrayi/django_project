from django.contrib import admin
from .models import Article, Category


def make_published(modeladmin, request, queryset):
    updated = queryset.update(status="p")
    if updated == 1:
        message_bit = "منتشر شد."
    else:
        message_bit = "منتشر شدند."
    modeladmin.message_user(request, "{} مقاله {}".format(updated, message_bit))

make_published.short_description = "انتشار مقالات انتخاب شده"

def make_draft(modeladmin, request, queryset):
    updated = queryset.update(status="d")
    if updated == 1:
        message_bit = "پیش نویس شد."
    else:
        message_bit = "پیس نویس شدند."
    modeladmin.message_user(request, "{} مقاله {}".format(updated, message_bit))

make_draft.short_description = "پیش نویس شدن مقالات انتخاب شده"

def make_active(modelcat, request, queryset):
    queryset.update(status = True)
make_active.short_description = "نمایش دسته بندی های انتخاب شده"

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("position","title","slug","status")
    list_filter = (["status"])
    search_fields= ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}
    actions = [make_active]

admin.site.register(Category, CategoryAdmin)

class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title","thumbnail_tag","slug","jpublish","status", "category_to_str")
    list_filter = ("publish","status")
    search_fields= ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("status", "publish")
    actions = [make_published, make_draft]

    def category_to_str(self, obj):
        return ", ".join([category.title for category in obj.category.active()])
    category_to_str.short_description = "دسته بندی"


admin.site.register(Article, ArticleAdmin)