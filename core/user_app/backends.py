from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.db.models import Q


User = get_user_model()
class EmailOrUsernameBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):  
        try:
            user = User.objects.get(Q(email__exact=username))
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None        

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except User.DoesNotExist:
            return None
