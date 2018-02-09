from django.conf.urls import url
from apps.user import views

urlpatterns = [
    url(r'^$', views.UserList.as_view(), name='user_list'),
    url(r'me^$', views.UserDetail.as_view(), name='user_detail'),
]
