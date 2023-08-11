from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.functions import Greatest, Least
from django.db.models import UniqueConstraint

User = get_user_model()


# Create your models here.
class Config(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    remote_account = models.CharField(max_length=64)
    local_account = models.CharField(max_length=64)
    txdelay = models.FloatField(default=2.0, validators=[
            MinValueValidator(1), MaxValueValidator(5)
    ])
    rxdelay = models.FloatField(default=5.0, validators=[
            MinValueValidator(1), MaxValueValidator(5)
    ])

    timeout = models.FloatField(default=60.0, validators=[
        MinValueValidator(1), MaxValueValidator(3600)
    ])
    last_ping = models.DateTimeField(auto_now=True)
    process_id = models.IntegerField(default=0)

    class Meta:
        constraints = [
            UniqueConstraint(
                Least('remote_account', 'local_account'),
                Greatest('remote_account', 'local_account'),
                name="unique_account_pair",
            )
        ]

    def get_pair(self):
        return [
            i.split(':')[0]
            for i in (self.remote_account, self.local_account)
        ]
