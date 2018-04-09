from django.conf.urls import url
from apps.user.views import UserListCreateView, UserDetailView, FacebookLogin

urlpatterns = [
    url(r'^$', UserListCreateView.as_view(), name='user_list'),
    url(r'^(?P<user_id>\d+)/?$', UserDetailView.as_view(), name='user_detail'),
    url(r'^fb_login/?$', FacebookLogin.as_view(), name='fb_login'),
]
