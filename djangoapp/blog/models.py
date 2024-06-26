"""
This module contains the `Tag` model, which represents a tag in the
application.

Classes:
    Tag
        A model representing a tag in the application.

Methods:
    save(*args, **kwargs)
        Override the default save method to generate a unique slug for the
        tag if it does not already have one.

"""
from django.db import models
from utils.rands import slugify_new
from utils.images import resize_image
from django.contrib.auth.models import User


class Tag(models.Model):
    """
    A model representing a tag in the application.

    Attributes:
        name (str): The name of the tag.
        slug (str): A unique slug for the tag.
    """
    class Meta:
        """
        Meta class for Django models.
        """
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    name = models.CharField(max_length=255)
    slug = models.SlugField(
        unique=True, default=None, null=True, blank=True,
        max_length=255,
    )

    def save(self, *args, **kwargs):
        """
        Override the default save method to generate a unique slug for the
        tag if it does not already have one.

        :param args: Additional positional arguments to be passed to the
        superclass's save method.
        :param kwargs: Additional keyword arguments to be passed to the
        superclass's save method.
        :return: None
        """
        if not self.slug:
            self.slug = slugify_new(self.name, 4)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.name)


class Category(models.Model):
    """
    A model representing a category in the application.

    Attributes:
        name (str): The name of the category.
        slug (str): A unique slug for the category.
    """
    class Meta:
        """
        Meta class for Django models.
        """
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=255)
    slug = models.SlugField(
        unique=True, default=None, null=True, blank=True,
        max_length=255,
    )

    def save(self, *args, **kwargs):
        """
        Override the default save method to generate a unique slug for the
        category if it does not already have one.

        :param args: Additional positional arguments to be passed to the
        superclass's save method.
        :param kwargs: Additional keyword arguments to be passed to the
        superclass's save method.
        :return: None
        """
        if not self.slug:
            self.slug = slugify_new(self.name, 4)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.name)


class Page(models.Model):
    class Meta:
        """
        Meta class for Django models.
        """
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'

    title = models.CharField(max_length=65)
    slug = models.SlugField(
        unique=True, default="", null=False, blank=True, max_length=255
    )
    is_published = models.BooleanField(
        default=False,
        help_text=(
            'Este campo precisará estar marcado'
            'para a página ser exibida publicamente.'
        ),
    )
    content = models.TextField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.title, 4)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.title)


class Post(models.Model):
    class Meta:
        """
        Meta class for Django models.
        """
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    title = models.CharField(max_length=65)
    slug = models.SlugField(
        unique=True, default="", null=False, blank=True, max_length=255
    )
    excerpt = models.CharField(max_length=150)
    is_published = models.BooleanField(
        default=False,
        help_text=(
            'Este campo precisará estar marcado'
            'para o post ser exibida publicamente.'
        ),
    )
    content = models.TextField()
    cover = models.ImageField(upload_to='posts/%Y/%m',
                              blank=True, default='')
    cover_in_post_content = models.BooleanField(
        default=True,
        help_text=('Se marcado, exibirá a capa dentro do post.'),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='post_created_by'
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='post_updated_by'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        default=None,
    )
    tags = models.ManyToManyField(Tag, blank=True, default='')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.title, 4)

        current_cover_name = str(self.cover.name)
        super_save = super().save(*args, **kwargs)
        cover_changed = False

        if self.cover:
            cover_changed = current_cover_name != self.cover.name

        if cover_changed:
            resize_image(self.cover, 900, True, 75)

        return super_save

    def __str__(self) -> str:
        return str(self.title)
