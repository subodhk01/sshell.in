from django.contrib.auth.decorators import user_passes_test

is_Verfied = user_passes_test( lambda u: u.is_verified, login_url="emailnotverified" )