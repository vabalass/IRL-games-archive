from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.conf import settings

class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    game = models.ForeignKey("games.Game", on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, related_name="replies")

    text = models.TextField(help_text="This game is...")
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    upvotes = models.PositiveSmallIntegerField(default=0)
    downvotes = models.PositiveSmallIntegerField(default=0)
    rating = models.PositiveSmallIntegerField(
        null = True, 
        blank = True, 
        help_text = "1-10",
        choices= [(i, i) for i in range(1, 11)], # from 1-10
        validators = [MinValueValidator(1), MaxValueValidator(10)], 
    )

    attachment = models.FileField(
        blank = True,
        null = True,
        upload_to ="comment_attachments/%Y/%m",
    )

    def clean(self):
        super().clean()
        if self.parent.game_id != self.game_id:
            raise ValidationError("Reply must be under the same Game as Parent.")
        
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.text[0:20] + ("..." if (len(self.text) > 20) else "")
