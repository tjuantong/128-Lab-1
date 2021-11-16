from django.contrib import admin
from draftwebivent.models import UserProfile, User
# Register your models here.


class ShowProfile(admin.ModelAdmin):
    model = UserProfile
    list_display = ['name', 'age', 'occupation', 'school', 'course_yr_lvl', 'interest', 'city', 'province', 'country']

admin.site.register(UserProfile, ShowProfile)

