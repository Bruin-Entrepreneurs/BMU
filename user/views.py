from django.shortcuts import render

from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView, CreateAPIView, mixins

# class UserListCreate(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
    # queryset = PFUser.objects.all()
    # serializer_class = PFUserListSerializer
    # permission_classes = [IsClient, ]

    # CREATE
    # def perform_create(self, serializer):
    #     username = serializer.validated_data['username']
    #     email = self.request.data['email']
    #     try:
    #         # TODO: need to enforce email uniqueness as well
    #         pf_user = PFUser.objects.get(username=username)
    #     except PFUser.DoesNotExist:
    #         try:
    #             pw = self.request.data['password']
    #             if pw == '':
    #                 raise exceptions.ParseError('empty password')
    #         except KeyError:
    #             raise exceptions.ParseError('missing password')
    #         pf_user = pf_user()
    #
    #     pf_user.username = username
    #     pf_user.display_name = username
    #     pf_user.email = email
    #     pf_user.set_password(pw)
    #     pf_user.is_staff = False
    #     pf_user.is_superuser = False
    #     pf_user.save()
    #     serializer.save(pf_user)
    #     Account.create(user=pf_user, confirm_email=False)
    #
    # # READ
    # def get(self, request, *args, **kwargs):
    #     username = self.request.query_params.get('username', '')
    #     email = self.request.query_params.get('email', '')
    #     either = self.request.query_params.get('any', '')
    #
    #     try:
    #         if username:
    #             user = PFUser.objects.get(username=username)
    #         elif email:
    #             user = PFUser.objects.get(user__email=email)
    #         elif either:
    #             user = PFUser.objects.get(
    #                 Q(user__email=either) | Q(username=either))
    #         else:
    #             return Response({'user': 'No search parameters provided.'}, status.HTTP_404_NOT_FOUND)
    #
    #         user.refresh_coins()
    #
    #         return Response({'user': True}, status.HTTP_200_OK)
    #     except PFUser.DoesNotExist:
    #         return Response({'user': False}, status.HTTP_200_OK)
    #
    # # UPDATE
    # @user_agent
    # @transaction.atomic
    # def post(self, request, *args, **kwargs):
    #     # Get referral code. Return error if referral code does not exist
    #     referral = None
    #     referral_code = request.data.get('referral_code', '')
    #     if referral_code != '':
    #         try:
    #             # Look up referral code
    #             referral = ReferralCode.objects.get(referral_code=referral_code)
    #         except ReferralCode.DoesNotExist:
    #             return Response({'error': 'Referral does not exist.'}, status.HTTP_200_OK)
    #
    #     # Response representing user
    #     try:
    #         response = self.create(request, *args, **kwargs)
    #     except ValidationError as exc:
    #         raise exc
    #
    #     if response.status_code != 201:
    #         return response
    #
    #     # fetch PF user
    #     user = self.get_queryset().filter(username=request.data['username'])[0]
    #
    #     logger.debug('Creating new user. Username: %s' % (user.username))
    #
    #     # fetch django user object
    #     django_user = PFUser.objects.get(username=user.username)
    #
    #     # Grant coins if there is a referer
    #     if referral_code != '':
    #         if referral.code_type == ReferralCode.USER_CODE:
    #             referred = Referred(referred_user=user, referred_by=referral)
    #             referred.save()
    #
    #             from_user = referral.from_user.first()
    #             logger.debug('New user has a pending referral. Referer %s and new user %s' % (
    #                 from_user.username, user.username,))
    #             # from_user.coins = (from_user.coins + 10)
    #             # from_user.save()
    #             # user.coins = user.coins + 10
    #             # user.save()
    #
    #             alert = playfull_api_models.Alert(
    #                 message='New user has a pending referral. Attributing both user %s and user %s with 10 coins.' % (
    #                     from_user.username, user.username,))
    #             alert.related_user = from_user
    #             alert.save()
    #
    #             # Create a new notification that tells the user about the bonus coins
    #             notification = Notification(owner=from_user, message='Your friend %s (%s) joined PlayFull!' % (
    #                 user.first_name, user.username))
    #             notification.save()
    #             notification = Notification(owner=user, message='You have been referred by your friend %s (%s)!' % (
    #                 from_user.first_name, from_user.username))
    #             notification.save()
    #         elif referral.code_type == ReferralCode.PROMO_CODE:
    #             # Apply promo code to user
    #             # TODO: Unshittify this
    #             handle_referral_code(user, referral)
    #
    #     # Create new access token
    #     access_token_string = common.generate_token()
    #     application = Application.objects.get(client_id='playfull_user')
    #     expires = (timezone.now() + datetime.timedelta(seconds=settings.OAUTH2_PROVIDER['ACCESS_TOKEN_EXPIRE_SECONDS']))
    #     scope = 'read write'
    #
    #     pf_access_token = AccessToken(user=django_user, token=access_token_string, application=application,
    #                                   expires=expires, scope=scope)
    #     pf_access_token.save()
    #
    #     # create new refresh token
    #     refresh_token_string = common.generate_token()
    #
    #     pf_refresh_token = RefreshToken(user=django_user, token=refresh_token_string, application=application,
    #                                     access_token=pf_access_token)
    #     pf_refresh_token.save()
    #
    #     # returned token needs to have the following fields:
    #     # (expires_in, refresh_token, access_token, token_type, scope)
    #     data = {'expires_in': settings.OAUTH2_PROVIDER['ACCESS_TOKEN_EXPIRE_SECONDS'],
    #             'refresh_token': refresh_token_string, 'access_token': access_token_string, 'token_type': 'Bearer',
    #             'scope': scope, }
    #     user_serializer = PFUserListSerializer(user)
    #     # TODO(roflcopterprime): DEVELOP MODE REFACTOR BELOW
    #     try:
    #         send_new_user_email(user)
    #     except:
    #         pass
    #     track_active_event(user.id)
    #
    #     return Response({'user': user_serializer.data, 'token': data}, status.HTTP_201_CREATED)