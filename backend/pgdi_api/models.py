from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    USER_TYPES = [
        ('contestant', 'Contestant'),
        ('creator', 'Creator'),
        ]
    
    user_type = models.CharField(max_length=10, choices=USER_TYPES,blank=True, default='contestant') #pode ser omitido mas se pretender ser creator tem de passar parametro

    def __str__(self):
        return self.username
    

class Contestant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Contestant: {self.user.username}"

class Creator(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Creator: {self.user.username}"
    
    
class Route(models.Model):
    creator=models.ForeignKey(Creator, on_delete=models.CASCADE)    
    file=models.FileField(upload_to='routes/')


class Competition(models.Model):
    name=models.CharField(max_length=50)
    start_date=models.DateTimeField()
    end_date=models.DateTimeField()
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE)
    routes = models.ManyToManyField(Route)
    constestants = models.ManyToManyField(User)

    def __str__(self):
        return self.name
        
        
class Submission(models.Model):
    file=models.FileField(upload_to='submissions/')
    contestant=models.ForeignKey(Contestant, on_delete=models.CASCADE)
    competition=models.ForeignKey(Competition, on_delete=models.CASCADE)
    score=models.FloatField()
    
    class Meta:
        unique_together = ('contestant', 'competition')