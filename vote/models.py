from django.db import models

class Vote(models.Model):
    user = models.ForeignKey(
        'votarkUser.VotarkUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )
    versus = models.ForeignKey(
        'versus.Versus',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )
    date = models.DateField()
    winner = models.BooleanField(null=False,blank=False)    #True for Right - False for left