from django.db import models
from django.db.models import Avg
from django.core.exceptions import ValidationError
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
    min_duration = models.PositiveSmallIntegerField(default=1) # minutes
    max_duration = models.PositiveSmallIntegerField(default=30)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.RESTRICT) # prevents deleting a Category if any Game references it

    environment = models.CharField(
        max_length = 4, 
        choices = Environment.choices, 
        default = Environment.OUTDOOR,
        help_text = "Where is this game best played?",
    )

    attachments = models.FileField(
        help_text = "Rules, printable game extras",
        blank = True,
        null = True,
        upload_to="game_attachments/%Y/%m",
    )

    equipment = TaggableManager(help_text="list of equipment (ball, string, paper...)", blank=True)

    def clean(self):
        super().clean()
        if self.min_players > self.max_players:
            raise ValidationError("Minimum players number cannot be bigger than maximum players.")
        if self.min_duration > self.max_duration:
            raise ValidationError("Minimum duration cannot be bigger than maximum duration.")
        
    def save(self, *args, **kwargs):
        # Force validation before saving to DB
        self.full_clean()

        # Call real save method
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Game"
        verbose_name_plural = "Games"
        ordering = ["title"] 

    def __str__(self):
        return self.title
    
    def equipment_list(self):
        return ", ".join(item.name for item in self.equipment.all())

class RecommendedGame(Game):
    class Meta:
        proxy = True # don't create new DB table
        verbose_name = "Recommended Game"
        verbose_name_plural = "Recommended Games"

    # bad because it sends query for every single Game 
    def average_rating(self):
        return (
            self.comments
            .filter(rating__isnull=False)
            .aggregate(avg=Avg("rating"))["avg"]
        ) or "No rating"
