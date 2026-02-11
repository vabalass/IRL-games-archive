from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Default custom user model for IRL games archive.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
    last_ip_address = models.GenericIPAddressField(null=True, blank=True)
    last_ip_update = models.DateTimeField(null=True, blank=True)

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    def update_ip(self, user_ip):
        yesterday = timezone.now() - timezone.timedelta(days=1)

        if self.last_ip_update is None or self.last_ip_update <= yesterday:
            self.last_ip_address = user_ip
            self.last_ip_update = timezone.now()
            self.save()
            return True

        return False
