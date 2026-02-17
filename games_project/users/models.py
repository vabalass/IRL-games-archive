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

    class Meta:
        ordering = ["-created"]
        verbose_name_plural = "User IPs"

    def __str__(self):
        return f"{self.user.username}: {self.ip_address}"

    @classmethod
    def save_ip_if_new(cls, user, ip_address):
        today = timezone.now().date()

        if cls.objects.filter(user=user, created__date=today).exists():
            return None

        return cls.objects.create(user=user, ip_address=ip_address)


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

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
