"""
Module for defining Django models for site setup and menu links.

This module contains two models: SiteSetup and MenuLink. The SiteSetup model
represents the site's setup, and the MenuLink model represents a link in the
site's menu.
"""
from django.db import models


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

    objects = models.Manager()

    def __str__(self) -> str:
        return str(self.title)
