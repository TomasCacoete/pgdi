from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import F
from django.db.models.functions import Rank
from django.db.models.expressions import Window

import backend.gpx_files.createSegment as createSegment
import backend.gpx_files.algoritmo as algoritmo

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
    score = models.IntegerField(blank=True, default=0)
    sprint_score = models.IntegerField(blank=True, default=0)
    mountain_score = models.IntegerField(blank=True, default=0)

    
    class Meta:
        unique_together = ('user', 'competition')
        
class Submission(models.Model):
    file = models.FileField(upload_to='submissions/', validators=[validate_gpx_file])
    contestant = models.ForeignKey(User, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    overall_time = models.DurationField(null=True, blank=True)
    sprint_time = models.DurationField(null=True, blank=True)

    class Meta:
        unique_together = ('contestant', 'competition')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the "real" save() method
        self.process_submission()

    def process_submission(self):
        # Assuming the competition has only one route for simplicity
        route = self.competition.routes.first()
        if route:
            overall_time, sprint_time, mountain_times, mountain_categories = algoritmo.check_route_passage(
                self.file.path, route.file.path
            )
            self.overall_time = overall_time
            self.sprint_time = sprint_time
            self.save(update_fields=['overall_time', 'sprint_time'])
            
            # Create MountainTime entries
            for i in range(len(mountain_times)):
                MountainTime.objects.create(
                    submission=self,
                    time = mountain_times[i],
                    category = mountain_categories[i]
                )

class MountainTime(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='mountain_times')
    time = models.DurationField()
    category = models.IntegerField()

@receiver(post_save, sender=Submission)
def update_user_competition_score(sender, instance, created, **kwargs):
    if created:
        competition = instance.competition
        
        # Overall classification
        overall_ranking = Submission.objects.filter(competition=competition).annotate(
            rank=Window(expression=Rank(), order_by=F('overall_time').asc())
        ).values('contestant', 'rank')

        # Sprint classification
        sprint_ranking = Submission.objects.filter(competition=competition).annotate(
            rank=Window(expression=Rank(), order_by=F('sprint_time').asc())
        ).values('contestant', 'rank')

        # Mountain classification
        mountain_points = {
            4: [1],                     # Fourth Category
            3: [2, 1],                  # Third Category
            2: [5, 3, 2, 1],            # Second Category
            1: [10, 8, 6, 4, 2, 1],     # First Category
            0: [20, 15, 12, 10, 8, 6, 4, 2]  # Hors Category
        }

        # Calculate mountain points
        for submission in Submission.objects.filter(competition=competition):
            mountain_score = 0
            for mountain_time in submission.mountain_times.all():
                category = mountain_time.category
                mountain_ranking = MountainTime.objects.filter(
                    submission__competition=competition,
                    category=category
                ).order_by('time')
                rank = list(mountain_ranking).index(mountain_time) + 1
                if rank <= len(mountain_points[category]):
                    mountain_score += mountain_points[category][rank - 1]
            
            # Update User_Competition
            user_comp, _ = User_Competition.objects.get_or_create(
                user=submission.contestant,
                competition=competition
            )
            
            overall_rank = next(r['rank'] for r in overall_ranking if r['contestant'] == submission.contestant.id)
            sprint_rank = next(r['rank'] for r in sprint_ranking if r['contestant'] == submission.contestant.id)
            
            user_comp.score = max(11 - overall_rank, 0) if overall_rank <= 10 else 0
            user_comp.sprint_score = (max(11 - sprint_rank, 0) if sprint_rank <= 10 else 0) + (user_comp.score * 2)
            user_comp.mountain_score = mountain_score
            user_comp.save()
