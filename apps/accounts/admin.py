from django.contrib import admin

from .models import (
    User,
    FreelancerProfile,
    EmployerProfile,
    Skill
)

admin.site.register(User)
admin.site.register(FreelancerProfile)
admin.site.register(EmployerProfile)
admin.site.register(Skill)