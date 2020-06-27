from django.utils import timezone

def email_verification(backend, user, response, *args, **kwargs):
    print("Backend :",backend)
    print("User :",user)
    print("response :",response)
    user.is_verified = True
    user.has_password = False
    user.last_send_verification_link = timezone.now()
    user.save()