from .models import Create_User
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status


# Create your tests here.


class TestUser(APITestCase):

    def setUp(self):
        """
            These are functions to be executed before (setUp) and after (tearDown) each unit test. These are very useful
             for fixtures.
        """
        """
            setup to test the User creation endpoint. In the method, we create a self. data containing
            all the data required to create a User and then make a POST request to the user/create endpoint with
             the payload.
        """
        self.data = {"username": "really", "password": "1233", "date_of_birth": "2000-5-7", "phone_number": "g96907t",
                     "street": "raj gad", "zip_code": "h34e3", "first_name": "Tiger", "last_name": "Lifer",
                     "email": "faugi2@gmail.com", "city": "Rahuri", "state": "marathoner", "country": "Zimbabwe"
                     }
        self.response = self.client.post(
            reverse('Users:profile_list'),
            self.data,
            format="json"
        )

    def test_Create_User(self):
        """
            This check Create User Test
        """
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_can_read_a_User(self):
        """
            This Function test the Read the user data
        """
        user = Create_User.objects.get()
        self.client.force_authenticate(user=user)
        response = self.client.get(
            reverse('Users:profile_Detail',
                    kwargs={'pk': user.id}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertContains(response, user)

    def test_can_update_a_user(self):
        """
            This is  tested user is updated
        """
        update_data = {"first_name": "Lion", "last_name": "Hell", }
        user = Create_User.objects.get()
        self.client.force_authenticate(user=user)

        response = self.client.patch(
            reverse('Users:profile_Detail',
                    args=[user.id]), update_data
        )
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_delete_a_User(self):
        """
            This test Case Use  to Delete  user
        """
        user = Create_User.objects.get()
        self.client.force_authenticate(user=user)
        response = self.client.delete(
            reverse('Users:profile_Detail',
                    kwargs={'pk': user.id}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # self.assertEqual(MyUser.objects.count(), 0)


class Test_login(APITestCase):
    def setUp(self):
        self.profile = Create_User.objects.create_user(
            username="really", password="1233", date_of_birth="2000-5-7", phone_number="g96907t",
            street="raj gad", zip_code="h34e3", first_name="Tiger", last_name="Lifer",
            email="faugi2@gmail.com", city="Rahuri", state="marathoner", country="Zimbabwe"
        )

    def test_can_login_a_User(self):
        """
            This is used to log in Valid-user test
        """
        user = Create_User.objects.get()
        self.client.force_authenticate(user=user)
        response = self.client.post(
            reverse('Users:login_user'),
            {"username": "really", "password": "1233", "email": "faugi2@gmail.com"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_try_login_invalid_User(self):
        """
             This is used to log in inValid-user test
        """
        user = Create_User.objects.get()
        self.client.force_authenticate(user=user)
        response = self.client.post(
            reverse('Users:login_user'),
            {"username": "reallied", "password": "332211", "email": "faugi2@gmail.com"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_can_try_invalid_user_retrieve(self):
        """
            test case for retrieve a record of user who is not logged in
        """
        response = self.client.get('Users:profile_Detail')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_try_invalid_user_update(self):
        """
            test case for update a record of user who is not logged in
        """
        response = self.client.put('Users:profile_Detail',
                                   {"first_name": "Dada", "last_name": "shamrock",
                                    "date_of_birth": "1998-05-11",
                                    "phone_number": 95553344,
                                    "street": "rewarding", "zip_code": 456372, "city": "PandaBoard", "state": "swa",
                                    "country": "USA"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_try_invalid_user_patch(self):
        """
            test case for partial update a record of user who is not logged in
        """
        response = self.client.patch('Users:profile_Detail', {"phone_number": 445566, "city": "attach"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_try_invalid_user_delete(self):
        """
            test case for delete a record of user who is not logged in
        """
        response = self.client.delete('Users:profile_Detail')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_try_can_try_anonymous_user(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(
            reverse('Users:login_user'),
            {"username": "Rbj", "password": "Kali", "email": "fa@gmail.com"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class Test_cases_for_Superuser(APITestCase):
    def setUp(self):
        self.super = Create_User.objects.create_superuser(
            username="Shubham1", password="2232", date_of_birth="2003-9-10", phone_number="72231t",
            street="read", zip_code="h3322", first_name="Right", last_name="Left",
            email="faf456@gmail.com", city="Rahu", state="planetary", country="Butane",  # is_superuser=True
        )
        self.profile = Create_User.objects.create_user(
            username="dgj", password="345", date_of_birth="2003-5-8", phone_number="dfv34",
            street="cd", zip_code="ce33", first_name="cdrwefcd", last_name="cdddqwcd",
            email="deft@gmail.com", city="cede", state="trews", country="imbiber"
        )
        # print(self.super)
        self.client.login(username="Shubham1", password="2232", email="faf456@gmail.com")

    def test_superuser_can_try_get_data(self):
        superuser = Create_User.objects.get(username="dgj")
        self.client.force_authenticate(user=superuser)
        response = self.client.get(
            reverse('Users:profile_Detail',
                    kwargs={'pk': superuser.id}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_super_can_update_a_user(self,):
        """
            This is  tested superuser is update user
        """
        update_data = {"first_name": "pad", "last_name": "bad", }
        superuser = Create_User.objects.get(username="dgj")
        self.client.force_authenticate(user=superuser)

        response = self.client.patch(
            reverse('Users:profile_Detail',
                    args=[superuser.id]), update_data
        )
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_delete_a_User(self):
        """
            This test Case Use  to Delete  superuser to  user
        """
        superuser = Create_User.objects.get(username="dgj")
        self.client.force_authenticate(user=superuser)
        response = self.client.delete(
            reverse('Users:profile_Detail',
                    kwargs={'pk': superuser.id}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # print(superuser.id)
