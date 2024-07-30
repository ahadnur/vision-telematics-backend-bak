from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth import get_user_model
from django.http import HttpResponse

User = get_user_model()


def activate(request, uidb64, token):
    try:
        uidb64 = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uidb64)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        user = None

    if user is not None and user.verification_token == token:
        user.is_active = True
        user.verification_token = None
        user.save()
        return HttpResponse('Thank you for your email confirmation. Your account is now activated.')
    else:
        return HttpResponse('Activation link is invalid!')
