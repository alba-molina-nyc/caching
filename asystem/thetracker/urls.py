from django.urls import URLPattern, path
from . import views


urlpatterns = [ 
    path('', views.memo, name='memo'),
    # passing in the job id we want to add to the memo
    path('add_memo/<int:job_id>/', views.add_memo, name='add_memo'),
]