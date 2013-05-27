__author__ = 'user'

from django.contrib.auth import get_user_model

User = get_user_model()


def validateEmail(email):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


class PersonAuthenticationBackend(object):
    def authenticate(self, username=None, password=None):
        user = None
        if validateEmail(username):
            try:
                user = User.objects.get(email__iexact=username)
            except User.DoesNotExist:
                pass

        if not user:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None

        if user and user.check_password(password):
            return user

        return None


    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


