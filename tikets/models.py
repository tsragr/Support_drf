from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey
from tikets.choices import Status


class Ticket(models.Model):
    """
    Ticket's model
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.TextField(choices=Status.choices, default=Status.active)

    def get_status(self, obj):
        return obj.get_status_display()

    def __str__(self):
        return f'{self.author.username} {self.status}'


class Answer(models.Model):
    """
    Answer's model
    """
    support = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='answer')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.support.username} {self.text}'


class Comment(MPTTModel):
    """
    Comment's model
    """
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = TreeForeignKey('self', verbose_name='parent', null=True, blank=True, related_name='children',
                            on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f'{self.user.username} {self.text[:50]}'
