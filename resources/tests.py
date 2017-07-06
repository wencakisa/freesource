from django.contrib.auth.models import User
from django.shortcuts import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from .models import Category, Resource, Comment


class AbstractTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username='test_user',
            password='passtestword123'
        )
        self.category = Category.objects.create(name='Test')

        self.unauthorized_message = 'Authentication credentials were not provided.'
        self.forbidden_message = 'You do not have permission to perform this action.'
        self.not_found_message = 'Not found.'


class CategoryListViewTestCase(AbstractTestCase):
    def setUp(self):
        super().setUp()

        self.url = reverse('resources:category-list')

        self.admin_user = User.objects.create_superuser(
            username='admin_user',
            email='admin@gmail.com',
            password='you1can2not3guess4my5password6'
        )

        self.post_data = {'name': 'Music'}

    def test_category_list_with_non_authenticated_user(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], self.unauthorized_message)

    def test_category_list_with_authenticated_user(self):
        self.client.force_authenticate(self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], self.category.id)
        self.assertEqual(response.data[0]['name'], self.category.name)

    def test_category_creation_with_non_authenticated_user(self):
        response = self.client.post(self.url, data=self.post_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], self.unauthorized_message)

    def test_category_creation_with_normal_user(self):
        self.client.force_authenticate(self.user)

        response = self.client.post(self.url, data=self.post_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], self.forbidden_message)

    def test_category_creation_with_admin_user(self):
        self.client.force_authenticate(self.admin_user)

        response = self.client.post(self.url, data=self.post_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(response.data['name'], Category.objects.last().name)


class ResourceAbstractTestCase(AbstractTestCase):
    def setUp(self):
        super().setUp()

        self.resource = Resource.objects.create(
            title='Test resource',
            resource_url='http://www.django-rest-framework.org/api-guide/testing/',
            owner=self.user
        )
        self.resource.categories.add(self.category)


class ResourceCategoryListTestCase(ResourceAbstractTestCase):
    def setUp(self):
        super().setUp()

        self.url_name = 'resources:resource-category-list'

    def test_resource_category_list_with_non_authorized_user(self):
        response = self.client.get(
            reverse(
                self.url_name,
                kwargs={'category_name': self.category.name.lower()}
            )
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], self.unauthorized_message)

    def test_resource_category_list_with_invalid_category(self):
        self.client.force_authenticate(self.user)

        response = self.client.get(
            reverse(
                self.url_name,
                kwargs={'category_name': 'wrong'}
            )
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], self.not_found_message)

    def test_resource_category_list_with_valid_category(self):
        self.client.force_authenticate(self.user)

        response = self.client.get(
            reverse(
                self.url_name,
                kwargs={'category_name': self.category.name.lower()}
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], self.resource.id)
        self.assertEqual(response.data[0]['categories'][0]['id'], self.category.id)


class ResourceViewSetTestCase(ResourceAbstractTestCase):
    def setUp(self):
        super().setUp()

        self.non_owner_user = User.objects.create_user(
            username='nonowner',
            password='123456789'
        )

        self.list_url_name = 'resources:resources-list'
        self.detail_url_name = 'resources:resources-detail'

        self.post_data = {
            'title': 'Sample title',
            'resource_url': 'http://www.diveintopython3.net/'
        }
        self.put_data = {
            'title': 'skydive'
        }

        self.forbidden_message = 'You are not the resource owner.'

    def test_resource_creation_with_non_authenticated_user(self):
        response = self.client.post(reverse(self.list_url_name), data=self.post_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], self.unauthorized_message)

    def test_resource_creation_with_authenticated_user(self):
        self.client.force_authenticate(self.user)

        response = self.client.post(reverse(self.list_url_name), data=self.post_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Resource.objects.count(), 2)

    def test_resource_list_with_non_authenticated_user(self):
        response = self.client.get(reverse(self.list_url_name))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], self.unauthorized_message)

    def test_resource_list_with_authenticated_user(self):
        self.client.force_authenticate(self.user)

        response = self.client.get(reverse(self.list_url_name))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], self.resource.title)

    def test_resource_detail_with_non_authenticated_user(self):
        response = self.client.get(
            reverse(
                self.detail_url_name,
                kwargs={'pk': self.resource.id}
            )
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], self.unauthorized_message)

    def test_resource_detail_with_authenticated_user(self):
        self.client.force_authenticate(self.user)

        response = self.client.get(
            reverse(
                self.detail_url_name,
                kwargs={'pk': self.resource.id}
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.resource.title)

    def test_resource_update_with_non_authenticated_user(self):
        response = self.client.put(
            reverse(
                self.detail_url_name,
                kwargs={'pk': self.resource.id}
            ),
            data=self.put_data
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], self.unauthorized_message)

    def test_resource_update_with_non_resource_owner(self):
        self.client.force_authenticate(self.non_owner_user)

        response = self.client.put(
            reverse(
                self.detail_url_name,
                kwargs={'pk': self.resource.id}
            ),
            data=self.put_data
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], self.forbidden_message)

    def test_resource_update_with_resource_owner(self):
        self.client.force_authenticate(self.resource.owner)

        response = self.client.put(
            reverse(
                self.detail_url_name,
                kwargs={'pk': self.resource.id}
            ),
            data=self.put_data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_resource_destroy_with_non_authenticated_user(self):
        response = self.client.delete(
            reverse(
                self.detail_url_name,
                kwargs={'pk': self.resource.id}
            )
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], self.unauthorized_message)

    def test_resource_destroy_with_non_resource_owner(self):
        self.client.force_authenticate(self.non_owner_user)

        response = self.client.delete(
            reverse(
                self.detail_url_name,
                kwargs={'pk': self.resource.id}
            )
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], self.forbidden_message)

    def test_resource_destroy_with_resource_owner(self):
        self.client.force_authenticate(self.resource.owner)

        response = self.client.delete(
            reverse(
                self.detail_url_name,
                kwargs={'pk': self.resource.id}
            )
        )

        self.assertFalse(Resource.objects.all())


class CommentViewSetTestCase(ResourceAbstractTestCase):
    def setUp(self):
        super().setUp()

        self.non_author_user = User.objects.create_user(
            username='non_author',
            password='iamnottheauthor123'
        )
        self.comment = Comment.objects.create(
            resource=self.resource,
            content='testestestest',
            author=self.user
        )

        self.list_url_name = 'resources:resource-comments-list'
        self.detail_url_name = 'resources:resource-comments-detail'

        self.post_data = {
            'content': 'blablablabla.'
        }

        self.forbidden_message = 'You can delete only your own comments.'

    def test_comment_creation_with_non_authenticated_user(self):
        response = self.client.post(
            reverse(
                self.list_url_name,
                kwargs={'resource_pk': self.resource.id}
            ),
            data=self.post_data
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], self.unauthorized_message)

    def test_comment_creation_with_authenticated_user(self):
        self.client.force_authenticate(self.user)

        response = self.client.post(
            reverse(
                self.list_url_name,
                kwargs={'resource_pk': self.resource.id}
            ),
            data=self.post_data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)

    def test_comment_list_with_non_authenticated_user(self):
        response = self.client.get(
            reverse(
                self.list_url_name,
                kwargs={'resource_pk': self.resource.id}
            )
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], self.unauthorized_message)

    def test_comment_list_with_authenticated_user(self):
        self.client.force_authenticate(self.user)

        response = self.client.get(
            reverse(
                self.list_url_name,
                kwargs={'resource_pk': self.resource.id}
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_comment_detail_with_non_authenticated_user(self):
        response = self.client.get(
            reverse(
                self.detail_url_name,
                kwargs={
                    'resource_pk': self.resource.id,
                    'pk': self.comment.id
                }
            )
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], self.unauthorized_message)

    def test_comment_detail_with_authenticated_user(self):
        self.client.force_authenticate(self.user)

        response = self.client.get(
            reverse(
                self.detail_url_name,
                kwargs={
                    'resource_pk': self.resource.id,
                    'pk': self.comment.id
                }
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], self.comment.content)

    def test_comment_update_with_non_authenticated_user(self):
        response = self.client.put(
            reverse(
                self.detail_url_name,
                kwargs={
                    'resource_pk': self.resource.id,
                    'pk': self.comment.id
                }
            ),
            data=self.post_data
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], self.unauthorized_message)

    def test_comment_update_with_non_comment_author(self):
        self.client.force_authenticate(self.non_author_user)

        response = self.client.put(
            reverse(
                self.detail_url_name,
                kwargs={
                    'resource_pk': self.resource.id,
                    'pk': self.comment.id
                }
            ),
            data=self.post_data
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], self.forbidden_message)

    def test_comment_update_with_comment_author(self):
        self.client.force_authenticate(self.comment.author)

        response = self.client.put(
            reverse(
                self.detail_url_name,
                kwargs={
                    'resource_pk': self.resource.id,
                    'pk': self.comment.id
                }
            ),
            data=self.post_data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_comment_destroy_with_non_authenticated_user(self):
        response = self.client.delete(
            reverse(
                self.detail_url_name,
                kwargs={
                    'resource_pk': self.resource.id,
                    'pk': self.comment.id
                }
            )
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], self.unauthorized_message)

    def test_comment_destroy_with_non_comment_author(self):
        self.client.force_authenticate(self.non_author_user)

        response = self.client.delete(
            reverse(
                self.detail_url_name,
                kwargs={
                    'resource_pk': self.resource.id,
                    'pk': self.comment.id
                }
            )
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], self.forbidden_message)


    def test_comment_destroy_with_comment_author(self):
        self.client.force_authenticate(self.comment.author)

        response = self.client.delete(
            reverse(
                self.detail_url_name,
                kwargs={
                    'resource_pk': self.resource.id,
                    'pk': self.comment.id
                }
            )
        )

        self.assertFalse(Comment.objects.all())
