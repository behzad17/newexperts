from django.test import TestCase, Client
from django.urls import reverse
from .models import User, ExpertProfile, PodcastProfile

class SimpleTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.expert_user = User.objects.create_user(username="expert", password="password", user_type="expert")
        self.podcaster_user = User.objects.create_user(username="podcaster", password="password", user_type="podcaster")
        self.expert_profile = ExpertProfile.objects.create(user=self.expert_user, name="Expert Name", bio="Expert Bio")
        self.podcast_profile = PodcastProfile.objects.create(user=self.podcaster_user, name="Podcast Name", description="Podcast Description")

    def test_home_page_status_code(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_profile_list_status_code(self):
        response = self.client.get(reverse("profile_list"))
        self.assertEqual(response.status_code, 200)

    def test_profile_detail_status_code(self):
        response = self.client.get(reverse("profile_detail", args=[self.expert_user.id]))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("profile_detail", args=[self.podcaster_user.id]))
        self.assertEqual(response.status_code, 200)

    def test_user_creation(self):
        self.assertEqual(User.objects.count(), 2)

    def test_profile_creation(self):
        self.assertEqual(ExpertProfile.objects.count(), 1)
        self.assertEqual(PodcastProfile.objects.count(), 1)
