from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from django.core.files.uploadedfile import SimpleUploadedFile
from backend.users.models import CustomUser
from models import Video, FavoriteList
from serializers import VideoSerializer
from unittest.mock import patch
from signals import convert_480p, convert_720p
from django.db.models.signals import post_delete, post_save


class VideoViewTests(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com", password="testpassword"
        )
        self.token = Token.objects.create(user=self.user)

    def test_get_videos(self):
        url = reverse("video-list")
        headers = {"HTTP_AUTHORIZATION": f"Token {self.token.key}"}

        video1 = Video.objects.create(
            title="Test Video 1", description="Description 1", is_validated=True
        )
        video2 = Video.objects.create(
            title="Test Video 2", description="Description 2", is_validated=True
        )

        response = self.client.get(url, **headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_post_video(self):
        url = reverse("video-list")
        headers = {"HTTP_AUTHORIZATION": f"Token {self.token.key}"}
        data = {
            "title": "New Test Video",
            "description": "New Test Description",
            "is_validated": True,
        }

        response = self.client.post(url, data, **headers)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Video.objects.count(), 1)
        self.assertEqual(Video.objects.first().title, "New Test Video")

    def test_post_invalid_video(self):
        url = reverse("video-list")
        headers = {"HTTP_AUTHORIZATION": f"Token {self.token.key}"}
        invalid_data = {"title": "", "description": "This is an invalid video"}

        response = self.client.post(url, invalid_data, **headers)

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data["status"])


class SearchViewTests(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com", password="testpassword"
        )
        self.token = Token.objects.create(user=self.user)

        self.video1 = Video.objects.create(
            title="Python Tutorial", description="Learn Python basics"
        )
        self.video2 = Video.objects.create(
            title="Django Tutorial", description="Learn Django framework"
        )

    def test_search_videos(self):
        url = reverse("search")
        headers = {"HTTP_AUTHORIZATION": f"Token {self.token.key}"}
        search_data = {"search_title": "python"}

        response = self.client.post(url, search_data, **headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Python Tutorial")

    def test_search_videos_no_value(self):
        url = reverse("search")
        headers = {"HTTP_AUTHORIZATION": f"Token {self.token.key}"}

        response = self.client.post(url, {}, **headers)

        self.assertEqual(response.status_code, 400)
        self.assertIn("Search value not provided", response.data)


class FavoriteListViewSetTests(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com", password="testpassword"
        )
        self.token = Token.objects.create(user=self.user)

        self.favorite_list1 = FavoriteList.objects.create(
            name="Favorites 1", user=self.user
        )
        self.favorite_list2 = FavoriteList.objects.create(
            name="Favorites 2", user=self.user
        )

    def test_get_favorite_lists(self):
        url = reverse("favorite-list-list")
        headers = {"HTTP_AUTHORIZATION": f"Token {self.token.key}"}

        response = self.client.get(url, **headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_create_favorite_list(self):
        url = reverse("favorite-list-list")
        headers = {"HTTP_AUTHORIZATION": f"Token {self.token.key}"}
        data = {"name": "New Favorites"}

        response = self.client.post(url, data, **headers)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(FavoriteList.objects.count(), 3)
        self.assertEqual(FavoriteList.objects.last().name, "New Favorites")


class FavoriteListViewTests(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com", password="testpassword"
        )
        self.token = Token.objects.create(user=self.user)

        self.favorite_list = FavoriteList.objects.create(owner=self.user)
        self.video1 = Video.objects.create(title="Video 1", description="Description 1")
        self.video2 = Video.objects.create(title="Video 2", description="Description 2")
        self.favorite_list.favorites.add(self.video1, self.video2)

    def test_post_with_user_id(self):
        url = reverse("favorite-list")
        headers = {"HTTP_AUTHORIZATION": f"Token {self.token.key}"}
        data = {"user_id": self.user.id}

        response = self.client.post(url, data, **headers)

        self.assertEqual(response.status_code, 200)
        self.assertIn("favorite_videos", response.data)
        self.assertIn("favorite_list", response.data)

        self.assertEqual(len(response.data["favorite_videos"]), 2)
        self.assertEqual(response.data["favorite_videos"][0]["title"], "Video 1")
        self.assertEqual(response.data["favorite_videos"][1]["title"], "Video 2")

    def test_post_without_user_id(self):
        url = reverse("favorite-list")
        headers = {"HTTP_AUTHORIZATION": f"Token {self.token.key}"}
        data = {}

        response = self.client.post(url, data, **headers)

        self.assertEqual(response.status_code, 400)
        self.assertIn("user_id is required", response.data["error"])


class VideoSignalTests(TestCase):

    @patch("myapp.signals.django_rq.get_queue")
    def test_video_post_save_signal(self, mock_get_queue):
        mock_queue_instance = mock_get_queue.return_value
        mock_enqueue = mock_queue_instance.enqueue

        video_file = SimpleUploadedFile(
            "video.mp4", b"file_content", content_type="video/mp4"
        )
        video = Video.objects.create(video_file=video_file)

        self.assertEqual(mock_enqueue.call_count, 2)
        mock_enqueue.assert_any_call(convert_480p, video.video_file.path)
        mock_enqueue.assert_any_call(convert_720p, video.video_file.path)


class VideoSignalTests(TestCase):

    @patch("myapp.signals.default_storage")
    def test_auto_delete_file_on_delete_signal(self, mock_default_storage):
        mock_delete = mock_default_storage.delete

        video_file = SimpleUploadedFile(
            "video.mp4", b"file_content", content_type="video/mp4"
        )
        thumbnail_file = SimpleUploadedFile(
            "thumbnail.jpg", b"thumbnail_content", content_type="image/jpeg"
        )
        video = Video.objects.create(video_file=video_file, thumbnail=thumbnail_file)

        post_delete.send(sender=Video, instance=video)

        mock_delete.assert_any_call(video.video_file.name)
        mock_delete.assert_any_call(video.thumbnail.name)


class VideoSignalTests(TestCase):

    @patch("myapp.signals.django_rq")
    def test_video_post_save_signal(self, mock_django_rq):
        mock_queue = mock_django_rq.get_queue.return_value
        mock_enqueue = mock_queue.enqueue

        video_file = SimpleUploadedFile(
            "video.mp4", b"file_content", content_type="video/mp4"
        )
        video = Video.objects.create(video_file=video_file)

        post_save.send(sender=Video, instance=video, created=True)

        mock_enqueue.assert_any_call(convert_480p, video.video_file.path)
        mock_enqueue.assert_any_call(convert_720p, video.video_file.path)
