from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    phone_no=models.CharField(max_length=15)
    
    USER_TYPES = [
        ('contestant', 'Contestant'),
        ('creator', 'Creator'),
        ]
    
    user_type = models.CharField(max_length=10, choices=USER_TYPES,blank=True, default='contestant') #pode ser omitido mas se pretender ser creator tem de passar parametro

    
    
    def __str__(self):
        return self.username

class Contestant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def customMethod(self):
        return f'sou um competidor'

class Creator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def customMethod(self):
        return f'sou um criador de competicoes'
    
    
class Competition(models.Model):
    name=models.CharField(max_length=50)
    start_date=models.DateTimeField()
    end_date=models.DateTimeField()
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE)

class Route(models.Model):
    creator=models.ForeignKey(Creator, on_delete=models.CASCADE)    
    file=models.FileField(upload_to='routes/')
    

class CompetitionRoute(models.Model):
    competition=models.ForeignKey(Competition, on_delete=models.CASCADE)
    route=models.ForeignKey(Route, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('competition', 'route')
        
        
class Submission(models.Model):
    file=models.FileField(upload_to='submissions/')
    contestant=models.ForeignKey(Contestant, on_delete=models.CASCADE)
    competition=models.ForeignKey(Competition, on_delete=models.CASCADE) # ? a
    score=models.FloatField()
    
    class Meta:
        unique_together = ('contestant', 'competition')