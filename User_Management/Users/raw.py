
#######

##$$$

# def destroy(self, request, *args, **kwargs):
"""
    This is used to when user  delete the other user  data then  show the error message
"""
#     if self.request.user.is_superuser:
#         return True
#     # elif self:
#     #     user = self.request.user
#     #     user.delete()
#     else:
#         return Response({"detail": 'You cannot delete this user'})
# def get_permissions(self):
#     # Your logic should be all here
#     if self.request.method == 'POST':
#         self.permission_classes = [UserPermission, ]
#     else:
#
#         return super(User_View, self).get_permissions()
#

#
# class User_detail_serializer(serializers.ModelSerializer):
#     model = Create_User
#     fields = [
#         'id', 'username', 'date_of_birth', 'phone_number',
#         'street', 'zip_code', 'email', 'city', 'state', 'country', 'first_name', 'last_name'
#     ]
#
# elif self.action in ['get']:
# return User_detail_serialize
#
#
#  def put(self, request, pk, token):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             try:
#                 user = Create_User.objects.get(pk=pk)
#                 token = PasswordResetTokenGenerator().check_token(user, token)
#                 if token:
#                     print(serializer.validated_data['password'])
#                     user.set_password(serializer.data.get('password'))
#                     user.save()
#                     return Response("Password Forget", status.HTTP_200_OK)
#                 else:
#                     return Response("activation Link Is Not Valid")
#             except(TypeError, ValueError, OverflowError, Create_User.DoesNotExistD):
#                 # user = None
#                 Response("Your Link Is Expired ")r
