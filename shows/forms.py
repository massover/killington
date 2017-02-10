from django.contrib.admin.helpers import ActionForm
from django.forms import fields


class EnterUserInLotteryForm(ActionForm):
    # Validation on ActionForms sucks. It just ends up saying
    # 'No action selected'. Let's do validation in the action view.
    email = fields.CharField(required=False)