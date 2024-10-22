from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Contestant)
admin.site.register(Creator)
admin.site.register(Competition)
admin.site.register(Route)
admin.site.register(CompetitionRoute)
admin.site.register(Submission)
