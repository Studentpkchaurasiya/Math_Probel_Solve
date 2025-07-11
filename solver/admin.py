from django.contrib import admin
from .models import Problem, UserProblemStatus, All_account


# Register your models here.
admin.site.register(All_account)
admin.site.register(Problem)
admin.site.register(UserProblemStatus)