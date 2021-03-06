from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('thetracker.urls')),
    path('memo', include('thetracker.urls')),
    path('add_memo', include('thetracker.urls')),
    path('add_memo/<int:job_id>/', include('thetracker.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('users/', include('users.urls')),

]