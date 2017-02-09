from django.contrib import admin
from .models import (
    Show,
    Performance,
    Lottery,
    User,
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    pass


@admin.register(Performance)
class ShowTimeAdmin(admin.ModelAdmin):
    pass


@admin.register(Lottery)
class LotteryAdmin(admin.ModelAdmin):
    pass
