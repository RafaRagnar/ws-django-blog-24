"""
Module for defining Django models for site setup and menu links.

This module contains two models: SiteSetup and MenuLink. The SiteSetup model
represents the site's setup, and the MenuLink model represents a link in the
site's menu.
"""
from django.db import models
from utils.model_validators import validate_png
from utils.images import resize_image


class MenuLink(models.Model):
    """
    MenuLink model represents a link in the site's menu.
    """
    class Meta:
        """
        Meta class for Django models.
        """
        verbose_name: str = 'Menu Link'
        verbose_name_plural: str = 'Menu Links'

    text: str = models.CharField(max_length=50)
    url_or_path: str = models.CharField(max_length=2048)
    new_tab: bool = models.BooleanField(default=False)
    site_setup = models.ForeignKey(
        'SiteSetup', on_delete=models.CASCADE,
        blank=True, null=True, default=None
    )

    def __str__(self) -> str:
        return str(self.text)


class SiteSetup(models.Model):
    """
    SiteSetup model represents the site's setup.
    """
    class Meta:
        """
        Meta class for Django models.
        """
        verbose_name: str = 'Setup'
        verbose_name_plural: str = 'Setup'

    title: str = models.CharField(max_length=65)
    description: str = models.CharField(max_length=255)

    show_header: bool = models.BooleanField(default=True)
    show_search: bool = models.BooleanField(default=True)
    show_menu: bool = models.BooleanField(default=True)
    show_description: bool = models.BooleanField(default=True)
    show_pagination: bool = models.BooleanField(default=True)
    show_footer: bool = models.BooleanField(default=True)

    favicon = models.ImageField(
        upload_to='assets/favicon/%Y/%m/',
        blank=True, default='',
        validators=[validate_png],
    )

    def save(self, *args, **kwargs):
        """
        Save the object and resize the favicon if it has changed.

        This method overrides the default `save` method to check if the
        favicon has changed. If the favicon has changed, it resizes the
        favicon to a width of 32 pixels.

        Args:
            *args: Positional arguments for the `save` method.
            **kwargs: Keyword arguments for the `save` method.
        """
        current_favicon_name = str(self.favicon.name)
        # print('current_favicon_name', current_favicon_name)
        super().save(*args, **kwargs)
        favicon_changed = False

        if self.favicon:
            favicon_changed = current_favicon_name != self.favicon.name

        # print('favicon_changed', favicon_changed)
        if favicon_changed:
            resize_image(self.favicon, 32)

    objects = models.Manager()

    def __str__(self) -> str:
        return str(self.title)
