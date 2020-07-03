from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

# is_Verfied = user_passes_test( lambda u: u.is_verified, login_url="emailnotverified/" )

def EmailVerified(function):
    def _function(request,*args, **kwargs):
        if not request.user.is_verified:
            return redirect('emailnotverified')
        return function(request, *args, **kwargs)
    return _function