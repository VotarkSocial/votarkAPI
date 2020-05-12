from django.db import models

class Post(models.Model):
    content = models.ImageField(null=False, blank=False)
    description = models.CharField(max_length=500)
    victories = models.IntegerField()
    date = models.DateField()
    order = models.ImageField()
    isMonetizedWeekly = models.BooleanField(default=False)
    isMonetizedMonthly = models.BooleanField(default=False)
    isMonetizedYearly = models.BooleanField(default=False)
    topic = models.ForeignKey(
        'topic.Topic',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )
    user = models.ForeignKey(
        'votarkUser.VotarkUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )