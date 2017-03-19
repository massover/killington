from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import (
    Show,
    Performance,
    Lottery,
    User,
)
from .forms import EnterUserInLotteryForm
from . import tasks


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'date_of_birth',
                    'zipcode', 'is_staff', )
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'date_of_birth', 'zipcode', )}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )


@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    actions = ['run_shows_spider']
    filter_horizontal = ('subscribed_users', )
    readonly_fields = ('slug', )

    def run_shows_spider(self, request, queryset):
        start_urls = queryset.values_list('url', flat=True)
        tasks.run_shows_spider.delay(start_urls=list(start_urls))
        count = queryset.count()
        if count == 1:
            message = 'Running spider for 1 show'
        else:
            message = 'Running spider for {} shows'.format(count)
        messages.success(request, message)

    run_shows_spider.short_description = "Run Spider For Shows"


@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'show', 'starts_at',)


@admin.register(Lottery)
class LotteryAdmin(admin.ModelAdmin):
    action_form = EnterUserInLotteryForm
    actions = ['enter_user_in_lottery', ]
    list_display = ('id', 'get_show_name', 'state', 'starts_at', 'ends_at',
                    'get_performance_starts_at',
                    'external_performance_id', 'nonce', 'get_entered_users_count',)
    filter_horizontal = ('entered_users', )

    def get_show_name(self, obj):
        return obj.performance.show.name

    get_show_name.short_description = 'Show Name'

    def get_performance_starts_at(self, obj):
        return obj.performance.starts_at

    get_performance_starts_at.short_description = 'Performance Starts At'

    def get_entered_users_count(self, obj):
        return obj.entered_users.count()

    get_entered_users_count.short_description = 'Entered Users'

    def enter_user_in_lottery(self, request, queryset):
        email = request.POST['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            message = 'User with email {} not found'.format(email)
            messages.error(request, message)
            return

        for lottery in queryset.all():
            tasks.enter_user_in_lottery.delay(user.id, lottery.id)

        message = 'Entering {} in the lottery'.format(user.email)
        messages.success(request, message)

    enter_user_in_lottery.short_description = "Enter user in lottery"
