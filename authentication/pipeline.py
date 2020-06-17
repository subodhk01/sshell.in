def email_verification(backend, user, response, *args, **kwargs):
    print("Backend :",backend)
    print("User :",user)
    print("response :",response)
    user.is_verified = True
    user.save()