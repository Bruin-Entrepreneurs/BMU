from django.conf.urls import url
from apps.user import views

urlpatterns = [
    url(r'^$', views.UserListCreateView.as_view(), name='user_list'),
    url(r'^me^$', views.UserDetailView.as_view(), name='user_detail'),
]
