from django.conf import settings
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models


class Comment(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )
    game = models.ForeignKey(
        "games.Game", on_delete=models.CASCADE, related_name="comments"
    )
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )

    text = models.TextField(help_text="This game is...")
    attachment = models.FileField(
        blank=True,
        null=True,
        upload_to="comment_attachments/%Y/%m",
    )
    rating = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="1-10",
        choices=[(i, i) for i in range(1, 11)],  # from 1-10
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )

    upvotes = models.PositiveSmallIntegerField(default=0)
    downvotes = models.PositiveSmallIntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created"]
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if self.parent_id and self.parent.game_id != self.game_id:
            msg = "Reply must be under the same Game as Parent."
            raise ValidationError(msg)

        if self.parent and self.parent.parent_id is not None:
            msg = "Cannot reply to a reply. Maximum nesting depth is 1."
            raise ValidationError(msg)

    def to_dict(self):
        return {
            "id": self.id,
            "author_name": self.author.username if self.author else "Anonymous",
            "text": self.text,
            "rating": self.rating or "-",
            "upvotes": self.upvotes,
            "downvotes": self.downvotes,
            "time_ago": naturaltime(self.created),
            "parent_id": self.parent_id,
        }

    @classmethod
    def get_all_for_game(cls, game_pk):
        comments = (
            cls.objects.filter(game__pk=game_pk, parent__isnull=True)
            .select_related("author")
            .prefetch_related("replies__author")
            .order_by("-created")
        )

        comments_with_replies = []
        for comment in comments:
            comment_dict = comment.to_dict()

            comment_dict["replies"] = [
                reply.to_dict() for reply in comment.replies.all().order_by("created")
            ]

            comments_with_replies.append(comment_dict)

        return comments_with_replies
