from django.db import models
from django.utils.timezone import now

class Signup(models.Model):  # Renamed to PascalCase (best practice)
    name = models.CharField(max_length=122)
    email = models.CharField(max_length=122, unique=True)
    youtube = models.CharField(max_length=255, null=True, blank=True, default="No YouTube Link")
    twitter = models.CharField(max_length=255, null=True, blank=True, default="No Twitter Link")
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class UserActivity(models.Model):
    user = models.ForeignKey(Signup, on_delete=models.CASCADE)
    login_time = models.DateTimeField(default=now)
    logout_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.name} - {self.login_time}"
