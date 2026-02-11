from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Avg
from django.utils import timezone
from taggit.managers import TaggableManager


class Environment(models.TextChoices):
    OUTDOOR = "OUT", "Outdoor"
    INDOOR = "IN", "Indoor"
    BOTH = "BOTH", "Indoor or Outdoor"


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, db_index=True)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["title"]

    def __str__(self):
        return self.title


class Game(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, db_index=True)
    description = models.TextField(help_text="Use markdown", blank=True)
    min_players = models.PositiveSmallIntegerField(default=1)
    max_players = models.PositiveSmallIntegerField(default=10)
    min_duration = models.PositiveSmallIntegerField(default=1)  # minutes
    max_duration = models.PositiveSmallIntegerField(default=30)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(
        Category, null=True, on_delete=models.RESTRICT
    )  # prevents deleting a Category if any Game references it
    is_active = models.BooleanField(
        default=True, help_text="Game can be deactivated without deleting it."
    )

    environment = models.CharField(
        max_length=4,
        choices=Environment,
        default=Environment.OUTDOOR,
        help_text="Where is this game best played?",
    )

    attachments = models.FileField(
        help_text="Rules, printable game extras",
        blank=True,
        null=True,
        upload_to="game_attachments/%Y/%m",
    )

    equipment = TaggableManager(
        help_text="list of equipment (ball, string, paper...)", blank=True
    )

    class Meta:
        verbose_name = "Game"
        verbose_name_plural = "Games"
        ordering = ["title"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Force validation before saving to DB
        self.full_clean()

        # Call real save method
        return super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if self.min_players > self.max_players:
            error = "Minimum players number cannot be bigger than maximum players."
            raise ValidationError(error)
        if self.min_duration > self.max_duration:
            error = "Minimum duration cannot be bigger than maximum duration."
            raise ValidationError(error)

    def equipment_list(self):
        return ", ".join(item.name for item in self.equipment.all())


class GameWithStats(Game):
    class Meta:
        proxy = True  # don't create new DB table
        verbose_name = "Game with stats"
        verbose_name_plural = "Games with stats"

    @property
    def average_rating(self):
        rating = self.comments.filter(rating__isnull=False).aggregate(
            avg=Avg("rating")
        )["avg"]

        return f"{rating:.2f}" if rating else "no rating"

    @property
    def last_comment(self):
        comment = self.comments.order_by("-created").first()
        return comment.text if comment else None

    yesterday = timezone.now() - timezone.timedelta(days=1)

    @property
    def comments_count_last_day(self):
        return self.comments.filter(created__gte=self.yesterday).count()

    @property
    def was_updated_last_day(self):
        return self.modified >= self.yesterday
