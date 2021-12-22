from django.db import models
import uuid
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    email = models.EmailField(max_length=254)
    created= models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.name)

class Website(models.Model):
    title = models.CharField(max_length=200)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    email=models.EmailField(max_length=254)
    url=models.URLField(default="http://127.0.0.1:8000",unique=True)
    monitored=models.BooleanField(default=True)
    timePeriod=models.IntegerField(default=4,validators=[MaxValueValidator(100), MinValueValidator(2)])
    owner = models.ManyToManyField(Profile, through='webData')
    def __str__(self):
        return self.title



class webData(models.Model):
    monitored=models.BooleanField(default=True)
    timePeriod=models.IntegerField(default=4,validators=[MaxValueValidator(100), MinValueValidator(2)])
    website=models.ForeignKey(Website, on_delete=models.CASCADE)
    profile= models.ForeignKey(Profile, on_delete=models.CASCADE)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    class Meta:
        unique_together = [['website', 'profile']]

    def __str__(self):
        return str(str(self.profile)+'  '+str(self.website))


class History(models.Model):
    webData = models.ForeignKey(webData,on_delete=models.CASCADE)
    statusCode= models.IntegerField(default=0)
    timestamp= models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    def __str__(self):
        return str(self.statusCode)