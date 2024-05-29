"""
Module for defining views related to the site setup.
"""
from site_setup.models import SiteSetup


def site_setup(request):
    """
    View function for retrieving the site setup object.

    This view function retrieves the most recent SiteSetup object from the
    database and returns it in the context as 'site_setup'.

    Returns:
        dict: A dictionary containing the site setup object.
    """
    setup = SiteSetup.objects.order_by('-id').first()
    return {
        'site_setup': setup,
    }
