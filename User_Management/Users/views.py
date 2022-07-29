from django.contrib.auth import login
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Create_User
from dj_rest_auth.views import LoginView

from .permissons import UserPermission
from .serializers import User_Serializer, User_Update_Serializer, Change_Password, Forget_password, New_Password
from rest_framework import status, viewsets, generics
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import AllowAny, IsAuthenticated


class User_View(viewsets.ModelViewSet):
    """
      A viewset.ModelViewSet that provides default `create()`, `retrieve()`, `update()`, `partial_update()`, `destroy()`
       and `list()` actions
    """
    queryset = Create_User.objects.all()
    serializer_class = User_Serializer
    permission_classes = [UserPermission, ]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('username', 'email', 'id')
    search_fields = ('first_name', 'last_name')

    def create(self, request, *args, **kwargs):
        """
             create method is used to create new data.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data1 = serializer.save()
            data1.is_active = False
            data1.save()
            currentsite = get_current_site(request)
            domain = currentsite.domain
            token = Token.objects.create(user=data1)
            subject = 'welcome to  My Project'
            message = f'Hi , thank you for registering.click link http://{domain}/activate/{data1.pk}/{token}'
            # print(message)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [data1.email, ]
            send_mail(subject, message, email_from, recipient_list)
            return Response({"detail": 'Confirm to check your mail to complete registation'},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        """
               Return the list of items for this view
        """
        if self.request.user.is_superuser:
            return Create_User.objects.all()
        else:
            """
            after get all products on DB it will be filtered by its owner and return the queryset
            """
            logged_in_user = Create_User.objects.filter(username=self.request.user.username)
            return logged_in_user

    def get_serializer_class(self):
        """
          This function write for overriding serializer
        """
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return User_Update_Serializer
        else:
            return self.serializer_class


@api_view(['GET'])
def activate(request, pk, token):
    try:
        data = Create_User.objects.get(pk=pk)
        fortoken = Token.objects.get(key=token)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        data = None
    if data is not None and fortoken:
        data.is_active = True
        data.save()
        # return redirect('Users')
        return Response("Thank you for your email confirmation. Now you can login your account.")
    else:
        return HttpResponse('Activation link is invalid!')


class CustomAuthToken(LoginView):
    """ for dj-rest-auth we have return user id with token """

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk
        })


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = Change_Password
    model = Create_User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Password_reset(generics.GenericAPIView):
    serializer_class = Forget_password
    permission_classes = [UserPermission]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email']
        user = Create_User.objects.filter(email=email).first()
        if user:
            pk = user.pk
            token = PasswordResetTokenGenerator().make_token(user)
            currentsite = get_current_site(request)
            domain = currentsite.domain
            subject = 'Forget Your Password'
            message = f'Hi ,Your forget password link is.click link http://{domain}/reset_password/{pk}/{token}'
            print(message)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            send_mail(subject, message, email_from, recipient_list)
            return Response({"detail": f'Go To Your Mail To password Forget  your password link '},
                            status=status.HTTP_410_GONE)
        else:
            return Response({"detail": 'User does not exit !! Please Enter The Correct email ...'},
                            status=status.HTTP_400_BAD_REQUEST)


class forget_password(generics.GenericAPIView):
    serializer_class = New_Password
    permission_classes = [AllowAny, ]

    def put(self, request, pk, token):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                user = Create_User.objects.get(pk=pk)
                token = PasswordResetTokenGenerator().check_token(user, token)
                if token:
                    print(serializer.validated_data['password'])
                    user.set_password(serializer.data.get('password'))
                    user.save()
                    return Response("Password Forget", status.HTTP_200_OK)
                else:
                    return Response("activation Link Is Not Valid")
            except(TypeError, ValueError, OverflowError, Create_User.DoesNotExistD):
                # user = None
                # Response("Your Link Is Expired ")
                pass
