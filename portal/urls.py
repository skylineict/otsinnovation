from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('skylinenow/', admin.site.urls),

     path('', include('homepage.urls')),
    path('reg/', include('registration.urls')),
    path('profile', include('userprofile.urls')),
    path('dashboard/', include("dash.urls")),
    path('courses/', include("courses.urls")),
    path('cohorts/', include("cohorts.urls")),
    path('projects/', include("projects.urls")),
    path('materials/', include("materials.urls")),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('credentail/', include('credential.urls')),
    path('send_email', include('emailssending.urls')),
    path('admindash/', include('admindash.urls')),
    path('newdash/', include('newdash.urls')),
    path('studenttask/', include('studenttask.urls')),
    path('facilitator/', include('facilitator.urls')),
     path('liveclass/', include('liveclass.urls')),
      path('monthlyscore/', include('monthlyscore.urls')),
     

   


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root = settings.MEDIA_ROOT)