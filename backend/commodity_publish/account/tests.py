from django.test import TestCase
from hashlib import sha256
from account.models import *
import random

# Create your tests here.
class UserTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        hasher = sha256()
        password = "1234"
        hasher.update(password.encode('utf-8'))
        password = hasher.hexdigest()
        User.objects.create(stuId="2017", password=password)

    def test_login(self):
        data = {"stuId":"2017", "password":"1234"}
        res = self.client.post("/users/login", data=data)
        self.assertEqual(res.status_code, 200)

    def test_logout(self):
        res = self.client.get("/users/logout")
        self.assertEqual(res.status_code, 200)

    def test_user_create(self):
        data = {
            "stuId": random.randint(2000,1000000),
            "password":"1234",
            "nickname":"milestin",
        }

        res = self.client.post("/users/", data=data)
        self.assertEqual(res.status_code, 200)

    def test_user_info_update(self):
        data = {
            "phone":"172341234",
            "campus":"1234",
            "class":"124",
        }

        res = self.client.put("/users/2017/")
        self.assertEqual(res.status_code, 200)

    def test_get_user_info(self):
        res = self.client.get("/users/2017")
        self.assertEqual(res.status_code, 200)
