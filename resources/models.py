from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(unique=True, max_length=50, blank=False)


    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Resource(models.Model):
    title = models.CharField(unique=True, max_length=255, blank=False)
    categories = models.ManyToManyField(Category, related_name='categories')
    resource_url = models.URLField(blank=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '\"{title}\" by {owner}'.format(title=self.title, owner=self.owner)


class Comment(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    content = models.CharField(max_length=255, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    posted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{class_name} for {resource_title} by {author_name}'.format(
            class_name=self.__class__.__name__,
            resource_title=self.resource.title,
            author_name=self.author.username
        )
