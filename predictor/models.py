from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):

    # Link prediction to logged-in user
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)

    phone = models.CharField(max_length=15)
    email = models.EmailField()

    symptoms = models.TextField()

    image = models.ImageField(upload_to='patients/')

    result = models.CharField(max_length=50, blank=True)

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name