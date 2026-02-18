from django import forms

from games_project.feedback.models import Comment

MIN_TEXT_LEN = 2
MAX_TEXT_LEN = 2000


class CommentForm(forms.ModelForm):
    parent = forms.IntegerField(required=False)

    class Meta:
        model = Comment
        fields = ["text"]

    def clean_text(self):
        text = self.cleaned_data.get("text", "").strip()

        if len(text) < MIN_TEXT_LEN:
            msg = f"Comment is too short (min {MIN_TEXT_LEN} characters)."
            raise forms.ValidationError(msg)

        if len(text) > MAX_TEXT_LEN:
            msg = f"Comment is too long (max {MAX_TEXT_LEN} characters)."
            raise forms.ValidationError(msg)

        return text

    def clean_parent(self):
        parent_id = self.cleaned_data.get("parent")

        if parent_id:
            try:
                parent = Comment.objects.get(id=parent_id)
            except Comment.DoesNotExist as e:
                msg = "Parent comment does not exist."
                raise forms.ValidationError(msg) from e
            else:
                if parent.parent_id is not None:
                    msg = "Cannot reply to a reply."
                    raise forms.ValidationError(msg)
                return parent

        return None
