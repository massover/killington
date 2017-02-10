from django.contrib import admin, messages

from .models import (
    Show,
    Performance,
    Lottery,
    User,
)
from .forms import EnterUserInLotteryForm
from . import tasks


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'date_of_birth',
                    'zipcode',)


@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ('show', 'starts_at', )


@admin.register(Lottery)
class LotteryAdmin(admin.ModelAdmin):
    action_form = EnterUserInLotteryForm
    actions = ['enter_user_in_lottery', ]
    list_display = ('performance', 'lottery_id', 'nonce', 'starts_at',
                    'processed',)

    def enter_user_in_lottery(self, request, queryset):
        email = request.POST['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            message = 'User with email {} not found'.format(email)
            messages.error(request, message)
            return

        for lottery in queryset.all():
            tasks.enter_user_in_active_lottery.delay(user.id, lottery.id)

        message = 'Entering {} in the lottery'.format(user.email)
        messages.success(request, message)

    enter_user_in_lottery.short_description = "Enter user in lottery"
