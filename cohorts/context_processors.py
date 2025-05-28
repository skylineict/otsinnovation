from cohorts.models import Cohort
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.contrib.auth import get_user_model
from userprofile.models import Profiles

user = get_user_model()

def get_cohorts(request):
    try:
       persoancohorts = Cohort.objects.get(users=request.user)
       return {'persoancohorts': persoancohorts}
    except:
        return {}
   
   


def get_profiles(request):
    try:
       profilesdatials = Profiles.objects.get(user=request.user)
       return {'allprofile': profilesdatials}
    except:
        return {}


def profile_get(request, pk):
    try:
       profilesnow = Profiles.objects.get(pk=pk)
       return {'myprofi': profilesnow}
    except:
        return {}

# class Cohorts(View):
#     def get_cohorts(self, request):
#        allcojrts = Cohorts.objects.get(users=request.user)
#        context = {'allcojrts':allcojrts}
#        return context
        