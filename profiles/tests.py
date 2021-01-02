import json
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status

from profiles.models import Profile, ProfileStatus
from profiles.serializers import ProfileSerializer, ProfileStatusSerializer, AvatarSerializer


class RegistrationTestCase(APITestCase):

    def test_registration(self):
        data = {"username":"techtester",
                "email":"hi@test.com",
                "password1":"Some_random_pass123",
                "password2":"Some_random_pass123"}
        response = self.client.post("/api/rest-auth/registration", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ProfileViewSetTestCase(APITestCase):

    list_url = reverse("profile-list")

    def setUp(self):
        self.user = User.objects.create_user(username = "tester",
                                             password = "some-random-strong-PASS123")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
    
    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION = "Token " + self.token.key)
    
    def test_profile_list_authenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_list_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    
    def test_profile_detail_retrieve(self):
        response = self.client.get(reverse("profile-detail", kwargs = {"pk":1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"], "tester")

    def test_profile_update_by_owner(self):
        response = self.client.put(reverse("profile-detail", kwargs = {"pk":1}),
                                   {"bio":"Newly updated","city":"Abuja"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), {"id": 1, "user":"tester",
                                                      "bio":"Newly updated",
                                                      "city":"Abuja", "avatar": None})

    def test_profile_update_by_randomuser(self):
        random_user = User.objects.create_user(username = "random",
                                             password = "some-random-strong-PASS456")
        self.client.force_authenticate(user=random_user)
        response = self.client.put(reverse("profile-detail", kwargs = {"pk":1}),
                                   {"bio":"Newly updated","city":"Abuja"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class StatusViewSetTestCase(APITestCase):

    list_url2 = reverse("status-list")

    def setUp(self):
        self.user = User.objects.create_user(username = "teststatus",
                                             password = "some-random-strong-PASS123")
        self.status = ProfileStatus.objects.create(user_profile=self.user.profile, 
                                                   status_content = "Status Testing")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
    
    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION = "Token " + self.token.key)
    
    def test_status_list_authenticated(self):
        response = self.client.get(self.list_url2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_status_list_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url2)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    
    def status_create(self):
        data = {"status_content":"Some random new status"}
        response = self.client.post(list_url2, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["user_profile"], "teststatus")
        self.assertEqual(response.data["status_content"], "Some random new status")

    def test_single_status_retrieve(self):
        serializer_data = ProfileStatusSerializer(instance = self.status).data
        response = self.client.get(reverse("status-detail", kwargs = {"pk":1}))
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, response_data)

    def test_status_update_owner(self):
        response = self.client.put(reverse("status-detail", kwargs = {"pk":1}),
                                   data = {"status_content":"Status Testing Updated"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status_content"], "Status Testing Updated")

    def test_status_update_random(self):
        random_user = User.objects.create_user(username = "random",
                                             password = "some-random-strong-PASS456")
        self.client.force_authenticate(user=random_user)
        response = self.client.put(reverse("status-detail", kwargs = {"pk":1}),
                                   data = {"status_content":"Status Testing Random"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
