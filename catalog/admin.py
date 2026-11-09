from django.contrib import admin

from .models import Category, Edition, Option, Poll, Vote


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 0


class PollInline(admin.TabularInline):
    model = Poll
    extra = 0


class OptionInline(admin.TabularInline):
    model = Option
    extra = 0


@admin.register(Edition)
class EditionAdmin(admin.ModelAdmin):
    list_display = ("year", "name")
    list_filter = ("year",)
    search_fields = ("name",)
    inlines = (CategoryInline,)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "edition")
    list_filter = ("edition",)
    search_fields = ("name", "description")
    inlines = (PollInline,)


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "status")
    list_filter = ("status", "category__edition")
    search_fields = ("title", "description", "category__name")
    inlines = (OptionInline,)


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ("name", "poll")
    list_filter = ("poll__category__edition", "poll__status")
    search_fields = ("name", "description", "poll__title")


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    """Read-only audit of stored votes."""

    list_display = ("user", "edition", "category", "poll", "option", "created_at")
    list_filter = ("edition", "category", "poll")
    search_fields = ("user__username", "option__name", "category__name")
    list_select_related = ("user", "edition", "category", "poll", "option")
    date_hierarchy = "created_at"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
