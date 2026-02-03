from django.db import models
from django.core.exceptions import ValidationError
from taggit.managers import TaggableManager

class Environment(models.TextChoices):
    OUTDOOR = "OUT", "Outdoor"
    INDOOR = "IN", "Indoor"
    BOTH = "BOTH", "Indoor or Outdoor"

class Game(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(help_text="Use markdown", blank=True)
    min_players = models.PositiveSmallIntegerField(default=1)
    max_players = models.PositiveSmallIntegerField(default=10)
    min_duration = models.PositiveSmallIntegerField(default=1) # minutes
    max_duration = models.PositiveSmallIntegerField(default=30)

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
        if self.min_players > self.max_players:
            raise ValidationError("Minimum players number cannot be bigger than maximum players.")
        if self.min_duration > self.max_duration:
            raise ValidationError("Minimum duration cannot be bigger than maximum duration.")
        
    def save(self, *args, **kwargs):
        # Force validation before saving to DB
        self.full_clean()

        # Call real save method
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Game"
        verbose_name_plural = "Gamesss"
        ordering = ["title"] 

    def __str__(self):
        return self.title