from accounts.models import UserProfile


def extras(request):
    if request.user.is_authenticated:
        profile= request.user.userprofile
        return {'profile':profile}
    else:
        return {}
