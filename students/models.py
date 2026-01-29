from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    passed_out = models.IntegerField()
    course = models.CharField(max_length=100)
    is_present = models.BooleanField(default=False)

    def __str__(self):
        return self.name