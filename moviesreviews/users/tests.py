from http import client
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files import File

from users.models import UserProfile

# Create your tests here.
class ProfileDetailsTest(TestCase):
    def test_access_my_private_page(self):
        me = User.objects.create(username='Me')
        me.set_password("MyPassword")
        me.save()

        my_profile = UserProfile()
        my_profile.user = me
        my_profile.profile_img.save("default.jpg", File(open("media/imgs/profileImgs/default.jpg", "rb")))
        my_profile.bio = "My bio"
        my_profile.is_user_page_public = False
        my_profile.save()

        self.client.login(username="Me", password="MyPassword")
        response = self.client.get(reverse('users:profile_details', args=[my_profile.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Pagina privata")

    def test_access_my_public_page(self):
        me = User.objects.create(username='Me')
        me.set_password("MyPassword")
        me.save()

        my_profile = UserProfile()
        my_profile.user = me
        my_profile.profile_img.save("default.jpg", File(open("media/imgs/profileImgs/default.jpg", "rb")))
        my_profile.bio = "My bio"
        my_profile.is_user_page_public = True
        my_profile.save()

        self.client.login(username="Me", password="MyPassword")
        response = self.client.get(reverse('users:profile_details', args=[my_profile.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Pagina privata")

    def test_access_to_user_detail_if_not_logged(self):
        me = User.objects.create(username='Me')
        me.set_password("MyPassword")
        me.save()

        my_profile = UserProfile()
        my_profile.user = me
        my_profile.profile_img.save("default.jpg", File(open("media/imgs/profileImgs/default.jpg", "rb")))
        my_profile.bio = "My bio"
        my_profile.is_user_page_public = True
        my_profile.save()

        response = self.client.get(reverse('users:profile_details', args=[my_profile.pk]))
        self.assertEqual(response.status_code, 302)

    def test_access_not_friend_private_page(self):
        me = User.objects.create(username='Me')
        me.set_password("MyPassword")
        me.save()

        my_profile = UserProfile()
        my_profile.user = me
        my_profile.profile_img.save("default.jpg", File(open("media/imgs/profileImgs/default.jpg", "rb")))
        my_profile.bio = "My bio"
        my_profile.is_user_page_public = True
        my_profile.save()

        other = User.objects.create(username='Other')
        other.set_password("OtherPassword")
        other.save()

        other_profile = UserProfile()
        other_profile.user = other
        other_profile.profile_img.save("default.jpg", File(open("media/imgs/profileImgs/default.jpg", "rb")))
        other_profile.bio = "other bio"
        other_profile.is_user_page_public = False
        other_profile.save()

        self.client.login(username="Me", password="MyPassword")
        response = self.client.get(reverse('users:profile_details', args=[other_profile.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pagina privata")

    def test_access_not_friend_public_page(self):
        me = User.objects.create(username='Me')
        me.set_password("MyPassword")
        me.save()

        my_profile = UserProfile()
        my_profile.user = me
        my_profile.profile_img.save("default.jpg", File(open("media/imgs/profileImgs/default.jpg", "rb")))
        my_profile.bio = "My bio"
        my_profile.is_user_page_public = True
        my_profile.save()

        other = User.objects.create(username='Other')
        other.set_password("OtherPassword")
        other.save()

        other_profile = UserProfile()
        other_profile.user = other
        other_profile.profile_img.save("default.jpg", File(open("media/imgs/profileImgs/default.jpg", "rb")))
        other_profile.bio = "other bio"
        other_profile.is_user_page_public = True
        other_profile.save()

        self.client.login(username="Me", password="MyPassword")
        response = self.client.get(reverse('users:profile_details', args=[other_profile.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Pagina privata")

    def test_access_friend_public_page(self):
        me = User.objects.create(username='Me')
        me.set_password("MyPassword")
        me.save()

        my_profile = UserProfile()
        my_profile.user = me
        my_profile.profile_img.save("default.jpg", File(open("media/imgs/profileImgs/default.jpg", "rb")))
        my_profile.bio = "My bio"
        my_profile.is_user_page_public = True
        my_profile.save()

        other = User.objects.create(username='Other')
        other.set_password("OtherPassword")
        other.save()

        other_profile = UserProfile()
        other_profile.user = other
        other_profile.profile_img.save("default.jpg", File(open("media/imgs/profileImgs/default.jpg", "rb")))
        other_profile.bio = "other bio"
        other_profile.is_user_page_public = True
        other_profile.save()

        other_profile.friends.set([my_profile])
        other_profile.save()

        self.client.login(username="Me", password="MyPassword")
        response = self.client.get(reverse('users:profile_details', args=[other_profile.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Pagina privata")

    def test_access_friend_private_page(self):
        me = User.objects.create(username='Me')
        me.set_password("MyPassword")
        me.save()

        my_profile = UserProfile()
        my_profile.user = me
        my_profile.profile_img.save("default.jpg", File(open("media/imgs/profileImgs/default.jpg", "rb")))
        my_profile.bio = "My bio"
        my_profile.is_user_page_public = True
        my_profile.save()

        other = User.objects.create(username='Other')
        other.set_password("OtherPassword")
        other.save()

        other_profile = UserProfile()
        other_profile.user = other
        other_profile.profile_img.save("default.jpg", File(open("media/imgs/profileImgs/default.jpg", "rb")))
        other_profile.bio = "other bio"
        other_profile.is_user_page_public = False
        other_profile.save()

        other_profile.friends.set([my_profile])
        other_profile.save()

        self.client.login(username="Me", password="MyPassword")
        response = self.client.get(reverse('users:profile_details', args=[other_profile.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Pagina privata")

    def test_admin_can_make_people_editor(self):
        admin = User.objects.create_superuser("admin", "admin@admin.it", "admin")
        admin.save()

        other = User.objects.create(username='Other')
        other.set_password("OtherPassword")
        other.save()

        other_profile = UserProfile()
        other_profile.user = other
        other_profile.profile_img.save("default.jpg", File(open("media/imgs/profileImgs/default.jpg", "rb")))
        other_profile.bio = "other bio"
        other_profile.is_user_page_public = False
        other_profile.save()

        self.client.login(username="admin", password="admin")
        response = self.client.get(reverse('users:profile_details', args=[other_profile.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Promuovi ad editore")
