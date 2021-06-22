from django.contrib import admin
from accounts.models import User,class_name
# Register your models here.
from django.utils.translation import ugettext_lazy as _
from inline_actions.actions import ViewAction
from inline_actions.admin import InlineActionsModelAdminMixin
from django.contrib import admin, messages

from django.core.mail import send_mail

class UnPublishActionsMixin(object):

    def get_inline_actions(self, request, obj=None):
        actions = super(UnPublishActionsMixin, self).get_inline_actions(request, obj)
        if obj and not obj.is_superuser:
            if obj.status == 0:
                actions.append('approve')
                actions.append('reject')
                actions.append('block')
                actions.append('unblock')

            elif obj.status == 1:
                actions.append('reject')
                actions.append('block')
            elif obj.status == 2:
                actions.append('unblock')
                actions.append('approve')

            elif obj.status == 3:
                actions.append('unblock')
                actions.append('approve')

            elif obj.status == 4:
                actions.append('approve')
                actions.append('reject')
                actions.append('block')

        return actions

    def approve(self, request, obj, parent_obj=None):
        obj.status = 1
        obj.save()
        subject = 'notification from admin to user'
        message = 'notification from admin to user '
        from_email = ['admin@gmail.com']
        recipient_list = [obj]
        send_mail(subject, message, from_email, recipient_list, fail_silently=True)

        messages.info(request, _("user approved."))

    approve.short_description = _("APPROVE")

    def reject(self, request, obj, parent_obj=None):
        obj.status = 2
        obj.save()
        messages.info(request, _("'REJECT"))
        hi = User.objects.all()

    reject.short_description = _("Reject")

    def block(self, request, obj, parent_obj=None):
        obj.status = 3
        obj.save()

        messages.info(request, _("user BLOCK."))

    block.short_description = _("BLOCK")

    def unblock(self, request, obj, parent_obj=None):
        obj.status = 3
        obj.save()

        messages.info(request, _("user UNBLOCK."))

    unblock.short_description = _("UNBLOCK")


class UsersAdmin(UnPublishActionsMixin, ViewAction, InlineActionsModelAdminMixin, admin.ModelAdmin):
    list_per_page = 20
    
    search_fields = ["class_name", "email", "date_of_birth"]
    list_filter = ("date_of_birth",)
    list_display = [ "email", "date_of_birth"]

    
    def get_queryset(self, request):
        return User.objects.order_by("-id")

    def save_model(self, request, obj, form, change):
        orig_obj = None
        if obj.id:
            orig_obj = User.objects.get(id=obj.id)
        if orig_obj:
            if orig_obj.check_password(obj.password):
                obj.set_password(obj.password)
        else:
            obj.set_password(obj.password)

        super().save_model(request, obj, form, change)
      

admin.site.register(User, UsersAdmin)
admin.site.register(class_name)