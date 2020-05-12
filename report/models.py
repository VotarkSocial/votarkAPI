from django.db import models

class Report(models.Model):
    content = models.ImageField(max_length=1000,null=False, blank=False)
    date = models.DateField()
    type = models.CharField(max_length=1000)
    user = models.ForeignKey(
        'votarkUser.VotarkUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )