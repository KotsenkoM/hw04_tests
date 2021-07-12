from django.test import TestCase

from ..models import User, Post, Group


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='z'
        )
        cls.user = User.objects.create(
            username='z',
        )
        cls.post = Post.objects.create(
            text='z' * 100,
            group=cls.group,
            author=cls.user,
        )

    def test_str_field(self):
        post = PostModelTest.post
        self.assertEqual(str(post), 'z' * 15)
