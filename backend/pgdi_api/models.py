from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

class User(AbstractUser):
    
    def __str__(self):
        return self.username
    
def validate_gpx_file(file):
    """Custom validator to check if the file has a .gpx extension."""
    if not file.name.endswith('.gpx'):
        raise ValidationError("Only .gpx files are allowed.")
    
    
class Route(models.Model):
    creator=models.ForeignKey(User, on_delete=models.CASCADE)    
    file=models.FileField(upload_to='routes/', validators=[validate_gpx_file])


class Competition(models.Model):
    name=models.CharField(max_length=50)
    start_date=models.DateTimeField()
    end_date=models.DateTimeField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    routes = models.ManyToManyField(Route)

    def __str__(self):
        return self.name

class User_Competition(models.Model): #table to connect directly user to an competition
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    score = models.FloatField(blank=True, default=0.0)

    class Meta:
        unique_together = ('user', 'competition')
        
class Submission(models.Model):
    file=models.FileField(upload_to='submissions/', validators=[validate_gpx_file])
    contestant=models.ForeignKey(User, on_delete=models.CASCADE)
    competition=models.ForeignKey(Competition, on_delete=models.CASCADE)
    overall_time = models.DurationField(null=True, blank=True)
    
    class Meta:
        unique_together = ('contestant', 'competition')