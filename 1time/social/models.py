from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Post(models.Model):
    body = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    author = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('author',)

    def __str__(self):
        return f'Post by {self.author.username}: {self.body[:20]}...'

    def save(self, *args, **kwargs):
        # Check if a post already exists for this author
        if Post.objects.filter(author=self.author).exists():
            raise ValidationError("You can only create one post.")
        super().save(*args, **kwargs)  # Call the original save method