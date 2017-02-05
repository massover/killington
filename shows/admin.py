from django.contrib import admin
from .models import (
    Show,
    ShowTime,
    Lottery,
    User,
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    pass


@admin.register(ShowTime)
class ShowTimeAdmin(admin.ModelAdmin):
    pass


@admin.register(Lottery)
class LotteryAdmin(admin.ModelAdmin):
    pass
