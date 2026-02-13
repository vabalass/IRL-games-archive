from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserIp(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ips",
    )
    ip_address = models.GenericIPAddressField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated"]
        verbose_name_plural = "User IPs"
        unique_together = ["user", "ip_address"]

    def __str__(self):
        return f"{self.user.username}: {self.ip_address}"

    @classmethod
    def save_ip_if_new(cls, user, ip_address):
        user_ip, is_new = cls.objects.get_or_create(
            user=user,
            ip_address=ip_address,
        )

        yesterday = timezone.now() - timedelta(days=1)
        if not is_new and user_ip.updated <= yesterday:
            user_ip.save()  # user_ip.updated field is updated
            return True
        if is_new:
            return True

        return bool(is_new)


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
