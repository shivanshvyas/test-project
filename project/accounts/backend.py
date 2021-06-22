from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

User = get_user_model()


class EmailBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            print(username,"sdf")
            user = User.objects.get(Q(email=username) | Q(username=username))
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            user.is_active = True
            
            user.set_password(password)
            user.save()
            return user
