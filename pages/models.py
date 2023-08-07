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
    delay = models.FloatField(default=1.0, validators=[
            MinValueValidator(1), MaxValueValidator(5)
    ])
    timeout = models.FloatField(default=60.0, validators=[
        MinValueValidator(1), MaxValueValidator(60)
    ])
    last_ping = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

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
