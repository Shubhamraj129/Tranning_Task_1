# from rest_framework import status
# from rest_framework.test import APITestCase
# from Users.models import UserDerived
# from django.urls import reverse
#
#
# # Create your tests here.
# # ORM queries Test Cases in detail
# class UserTest(APITestCase):
#
#     def setUp(self):
#         self.user = UserDerived.objects.create_user(first_name="Priti", last_name="Nakade", username="priti",
#                                                     email="pritipalaskar23@gmail.com", password="priti",
#                                                     date_of_birth='1990-01-23', phone_number=9876545365,
#                                                     street="MG Road",
#                                                     city="Pune", state="Maharashtra", country="India", zip_code=412105)
#         self.other_user = UserDerived.objects.create_user(first_name="Datta", last_name="Nakade", username="datta",
#                                                           email="datta23@gmail.com", password="datta",
#                                                           date_of_birth='1990-10-10', phone_number=9872314125,
#                                                           street="MG Road",
#                                                           city="Pune", state="Maharashtra", country="India",
#                                                           zip_code=412105)
#
#         self.user_detail_url = reverse("user-detail", args=[self.user.id])
#         self.other_user_url = reverse("user-detail", args=[self.other_user.id])
#         self.user_login_url = reverse("login")
#         self.client.force_authenticate(user=self.user)
#
#     def test_user_register(self):
#         """
#             test case for user_register
#         """
#         expected_data = {"first_name": "Priti", "last_name": "Nakade", "username": "priti@23", "password": "priti@23",
#                          "date_of_birth": "1990-01-23", "email": "priti@gmail.com", "phone_number": 7865456755,
#                          "street": "SBRoad", "zip_code": 412105, "city": "Pune", "state": "Maharashtra",
#                          "country": "India"
#                          }
#         response = self.client.post('/user_register/', expected_data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_user_retrieve(self):
#         """
#             test case for retrieve a record of user
#         """
#         response = self.client.get(self.user_detail_url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_update_user(self):
#         """
#             test case for update a record of user
#         """
#         response = self.client.put(self.user_detail_url,
#                                    {"first_name": "Priti", "last_name": "Nakade",
#                                     "date_of_birth": "1990-01-23",
#                                     "phone_number": 7867856755,
#                                     "street": "SBRoad", "zip_code": 412105, "city": "Mumbai", "state": "Maharashtra",
#                                     "country": "India"})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_patch_user(self):
#         """
#             test case for partial update a record of user
#         """
#         response = self.client.patch(self.user_detail_url, {"phone_number": 7867566755, "city": "Mumbai"})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_delete_user(self):
#         """
#             test case for delete a record of user
#         """
#         response = self.client.delete(self.user_detail_url)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#
#     def test_login_user(self):
#         """
#             test case for login a registered user
#         """
#         response = self.client.post(self.user_login_url, {"username": "priti", "email": "pritipalaskar23@gmail.com",
#                                                           "password": "priti "})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_login_anonymous_user(self):
#         """
#             test case for login anonymous user
#         """
#         self.client.force_authenticate(user=None)
#         response = self.client.post(self.user_login_url, {"username": "pritin", "email": "pritipalaskar@gmail.com",
#                                                           "password": "pritin "})
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#
#     def test_invalid_login_user(self):
#         """
#             test case for login a non-registered user
#         """
#         response = self.client.post(self.user_login_url, {"username": "priti", "email": "pritipalaskar23@gmail.com",
#                                                           "password": "priti23"})
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#
#     def test_invalid_user_retrieve(self):
#         """
#             test case for retrieve a record of user who is not logged in
#         """
#         response = self.client.get(self.other_user_url)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#
#     def test_invalid_user_update(self):
#         """
#             test case for update a record of user who is not logged in
#         """
#         response = self.client.put(self.other_user_url,
#                                    {"first_name": "Datta", "last_name": "Nakade",
#                                     "date_of_birth": "1990-01-23",
#                                     "phone_number": 9872314125,
#                                     "street": "SBRoad", "zip_code": 412105, "city": "Mumbai", "state": "Maharashtra",
#                                     "country": "India"})
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#
#     def test_invalid_user_patch(self):
#         """
#             test case for partial update a record of user who is not logged in
#         """
#         response = self.client.patch(self.other_user_url, {"phone_number": 9872314125, "city": "Mumbai"})
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#
#     def test_invalid_user_delete(self):
#         """
#             test case for delete a record of user who is not logged in
#         """
#         response = self.client.delete(self.other_user_url)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#
#
# class SuperUserTest(APITestCase):
#     def setUp(self):
#         self.superuser = UserDerived.objects.create_superuser(username="pritin",
#                                                               email="pritin@gmail.com", password="pritin",
#                                                               date_of_birth='1990-10-10')
#         self.assertEqual(self.superuser.email, 'pritin@gmail.com')
#         self.assertTrue(self.superuser.is_active)
#         self.assertTrue(self.superuser.is_staff)
#         self.assertTrue(self.superuser.is_superuser)
#
#         self.user = UserDerived.objects.create_user(first_name="Priti", last_name="Nakade", username="priti",
#                                                     email="pritipalaskar23@gmail.com", password="priti",
#                                                     date_of_birth='1990-01-23', phone_number=9876545365,
#                                                     street="MG Road",
#                                                     city="Pune", state="Maharashtra", country="India", zip_code=412105)
#
#         self.superuser_detail_url = reverse("user-detail", args=[self.user.id])
#         self.user_all_url = reverse("user-list")
#         self.superuser_login_url = reverse("login")
#         self.client.force_authenticate(user=self.superuser)
#
#     def test_login_superuser(self):
#         """
#             test case for login a registered user
#         """
#         response = self.client.post(self.superuser_login_url, {"username": "pritin", "email": "pritin@gmail.com",
#                                                                "password": "pritin "})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_retrieve_list(self):
#         response = self.client.get(self.user_all_url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_update_superuser(self):
#         response = self.client.put(self.superuser_detail_url,
#                                    {"first_name": "Priti", "last_name": "Nakade",
#                                     "date_of_birth": "1990-01-23",
#                                     "phone_number": 7867856755,
#                                     "street": "SBRoad", "zip_code": 412105, "city": "Mumbai", "state": "Maharashtra",
#                                     "country": "India"})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_patch_user(self):
#         """
#             test case for partial update a record of user
#         """
#         response = self.client.patch(self.superuser_detail_url, {"phone_number": 7867566755, "city": "Mumbai"})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_delete_superuser(self):
#         response = self.client.delete(self.superuser_detail_url)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)




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