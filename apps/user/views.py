import logging
from collections import defaultdict
from typing import Dict
import requests
import json
from braces.views import CsrfExemptMixin

from django.conf import settings
from django.utils import timezone
from django.db.models.query_utils import Q
from oauth2_provider.models import Application, AccessToken, RefreshToken
from oauth2_provider.settings import oauth2_settings
from oauth2_provider.views.mixins import OAuthLibMixin
from oauthlib import common
from oauthlib.oauth2 import Server
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.helpers.helpers import get_data_field_or_400
from apps.user.models import User
from apps.user.serializer import UserSerializer, UserSummarySerializer

logger = logging.getLogger(__name__)


class UserListCreateView(ListCreateAPIView):
    queryset = User.objects.all().exclude(username='bmu_user')
    serializer_class = UserSummarySerializer


class UserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        user_instance = self.get_queryset().get(pk=self.kwargs['user_id'])
        serializer = self.get_serializer(user_instance)

        return Response(serializer.data)


# facebook login
class FacebookLogin(GenericAPIView):
    permission_classes = []
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        fb_token = get_data_field_or_400(request, 'fb_token')
        notification_token = get_data_field_or_400(request, 'notification_token')
        app_access_token = settings.FB_APP_ID + '|' + settings.FB_APP_SECRET
        params = {
            'input_token': fb_token,
            'access_token': app_access_token
        }

        r = requests.get(
            'https://graph.facebook.com/{version}/debug_token'.format(version=settings.FACEBOOK_GRAPH_VERSION),
            params=params,
        )

        data = r.json()['data']
        is_valid = data['is_valid']
        fb_app_id = str(data['app_id'])
        fb_user_id = data['user_id']
        expires_at = data['expires_at']

        # verify that the token is valid and that the app IDs match
        if is_valid and fb_app_id == settings.FB_APP_ID:
            # Query db and try to find user
            try:
                user = User.objects.get(facebook_id=fb_user_id)
                user.notification_token = notification_token
                user.save()

                user_data = self.get_serializer(user).data
                token_data = create_token(user)
                data = {
                    'user': user_data,
                    'token': token_data
                }

                return Response(data=data, status=status.HTTP_201_CREATED)
            except User.DoesNotExist:
                params = {
                    'access_token': fb_token
                }

                r = requests.get(
                    'https://graph.facebook.com/{version}/me?fields=id,first_name,last_name,email'.format(
                        version=settings.FACEBOOK_GRAPH_VERSION),
                    params=params,
                )

                # check that the request was successful
                if r.status_code == requests.codes.ok:
                    data = defaultdict(lambda: '', r.json())

                    _id = data['id']
                    _first_name = data['first_name']
                    _last_name = data['last_name']
                    _email = data['email']
                    _profile_pic_url = 'https://graph.facebook.com/{id}/picture?type=large'.format(id=_id)

                    # Create unique username lmao
                    _username = _first_name
                    if User.objects.filter(username=_username).count() >= 1:
                        count = 1

                        while User.objects.filter(username=_username + str(count)).count() >= 1:
                            count += 1

                        _username += str(count)

                    user = User.objects.create(
                        username=_username,
                        first_name=_first_name,
                        last_name=_last_name,
                        email=_email,
                        profile_pic_url=_profile_pic_url,
                        facebook_id=_id,
                        notification_token=notification_token
                    )
                    user.set_unusable_password()
                    user.save()

                    user_data = self.get_serializer(user).data
                    token_data = create_token(user)
                    data = {
                        'user': user_data,
                        'token': token_data
                    }

                    return Response(data=data, status=status.HTTP_201_CREATED)
                else:
                    logger.debug('Failed to fetch facebook user info for facebook ID: ' + str(fb_user_id))
                    return Response('Failed to fetch facebook user info.',
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            logger.debug("facebook token failed with isvalid:" + str(is_valid) + ",fb_app_id:" + str(
                fb_app_id) + ",fb_user_id:" + str(fb_user_id) + ",expires_at:" + str(expires_at))
            return Response('input_token is invalid.', status=status.HTTP_400_BAD_REQUEST)


# Access token generation
class OAuthToken(OAuthLibMixin, CsrfExemptMixin, APIView):
    server_class = Server
    validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS
    oauthlib_backend_class = oauth2_settings.OAUTH2_BACKEND_CLASS
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        grant_type = get_data_field_or_400(request, 'grant_type')
        user_id = get_data_field_or_400(request, 'user_id')

        print('HERE')
        url, headers, body, status = self.create_token_response(request)
        print('HERE AGAIN')
        response_json = {}

        token_json = json.loads(body)
        response_json['token'] = token_json

        try:
            error = token_json['error']
        except KeyError:
            # if 'password' grant type, insert user info into response
            if grant_type == 'password':
                user = User.objects.get(pk=user_id)
                user_json = UserSerializer(user)
                response_json['user'] = user_json.data

                # erase all existing access tokens that belong to the user
                tokens = AccessToken.objects.filter(user=user).exclude(token=token_json['access_token'])
                tokens.delete()
            elif grant_type == 'refresh_token':
                token_string = token_json['refresh_token']
                refresh_token = RefreshToken.objects.get(token=token_string)
                user = refresh_token.user

                # erase all existing access tokens that belong to the user
                tokens = AccessToken.objects.filter(user=user).exclude(token=token_json['access_token'])
                tokens.delete()
            elif grant_type == 'client_credentials':
                # delete expired client access tokens
                tokens = AccessToken.objects.filter(user=None, expires__lte=timezone.now())
                tokens.delete()

        body = response_json
        return Response(data=body, status=status)


# Returns a body that lists authentication details
def create_token(user: User) -> Dict:
    # erase all existing access tokens that belong to the user
    tokens = AccessToken.objects.filter(user=user)
    tokens.delete()

    application = Application.objects.get(client_id='bmu_user')
    expires = (
        timezone.now() + timezone.timedelta(
            seconds=settings.OAUTH2_PROVIDER['ACCESS_TOKEN_EXPIRE_SECONDS']))
    scope = 'read write'

    # Create access token
    access_token_string = common.generate_token()
    bmu_access_token = AccessToken(
        user=user,
        token=access_token_string,
        application=application,
        expires=expires,
        scope=scope
    )
    bmu_access_token.save()

    # Create refresh token
    refresh_token_string = common.generate_token()
    bmu_refresh_token = RefreshToken(
        user=user,
        token=refresh_token_string,
        application=application,
        access_token=bmu_access_token
    )
    bmu_refresh_token.save()

    data = {
        'expires_in': settings.OAUTH2_PROVIDER['ACCESS_TOKEN_EXPIRE_SECONDS'],
        'refresh_token': refresh_token_string,
        'access_token': access_token_string,
        'token_type': 'Bearer',
        'scope': scope
    }

    return data
