from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post, User


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='AndreyG')
        cls.group = Group.objects.create(
            title='Тестовый текст',
            slug='test_slug'
        )
        cls.post = Post.objects.create(
            text='Тестовый текст',
            group=cls.group,
            author=cls.user
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post_for_guest(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Текст из формы',
            'group': self.group
        }
        self.guest_client.post(
            reverse('new_post'),
            data=form_data,
            follow=True,
        )
        self.assertEqual(Post.objects.count(), posts_count)

    def test_create_post_for_auth_user(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Текст из формы',
            'group': self.group.id
        }
        self.authorized_client.post(
            reverse('new_post'),
            data=form_data,
            follow=True
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(self.user.posts)

    def test_edit_post(self):
        form_data = {
            'text': 'Другой текст',
        }
        self.authorized_client.post(
            reverse('post_edit', kwargs={
                'username': self.user.username,
                'post_id': self.post.id,
            }),
            data=form_data,
            follow=True
        )
        self.assertTrue(self.user.posts.filter)
