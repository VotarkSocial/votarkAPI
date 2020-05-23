from django.db import models
from django.utils.timezone import now
from django.core.exceptions import ValidationError

class Post(models.Model):
    image = models.ImageField(null=True, blank=True)
    video = models.FileField(upload_to='videos/', null=True, verbose_name="")
    description = models.CharField(max_length=500,null=True)
    victories = models.IntegerField(null=False, default=0)
    date = models.DateTimeField(default=now)
    order = models.IntegerField(null=True)
    topic = models.ForeignKey(
        'topic.Topic',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    user = models.ForeignKey(
        'votarkUser.VotarkUser',
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    def clean(self):
        super().clean()
        if self.image is None and self.video is None:
            raise ValidationError('image and video are both None')