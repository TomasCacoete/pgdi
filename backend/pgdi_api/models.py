from django.db import models

# Create your models here.



class Competition(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    # creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Route(models.Model):
    id = models.AutoField(primary_key=True)
    # file = models.FileField(upload_to='routes/')

    def __str__(self):
        return self.name

class Competition_Route(models.Model):
    route_id = models.ForeignKey(Route, on_delete=models.CASCADE)
    competition_id = models.ForeignKey(Competition, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Submission(models.Model):
    route_id = models.ForeignKey(Route, on_delete=models.CASCADE)
    contestant_competition_id = 
    # submission_file = models.FileField(upload_to='submissions/')
