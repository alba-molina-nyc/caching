from django.urls import URLPattern, path
from . import views


urlpatterns = [ 
   
    path('', views.memo, name='memo'),
    # passing in the job id we want to add to the memo
    path('add_memo/<int:job_id>/', views.add_memo, name='add_memo'),
    path('remove_memo_item/<int:job_id>/', views.remove_memo_item, name='remove_memo_item'),
]



# urlpatterns = [
#     path('', views.memo, name='memo'),
#     path('add_memo/<int:job_id>/', views.add_memo, name='add_memo'),
#     path('remove_memo/<int:job_id>/<int:memo_item_id>/', views.remove_memo, name='remove_memo'),
#     path('remove_memo_item/<int:job_id>/<int:memo_item_id>/', views.remove_memo_item, name='remove_memo_item'),

#     path('checkout/', views.checkout, name='checkout'),
# ]