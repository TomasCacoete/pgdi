from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Contestant)
admin.site.register(Creator)
admin.site.register(Route)
admin.site.register(Submission)
admin.site.register(Competition)