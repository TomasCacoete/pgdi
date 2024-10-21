from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name
    

class Contestant(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Contestant: {self.user.name}"

class Creator(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Creator: {self.user.name}"


class Route(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name
    

class Submission(models.Model):
    route_id = models.ForeignKey(Route, on_delete=models.CASCADE)
    contestant_id = models.ForeignKey(Contestant, on_delete=models.CASCADE)
    

class Competition(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    routes = models.ManyToManyField(Route)
    
    def __str__(self):
        return self.name