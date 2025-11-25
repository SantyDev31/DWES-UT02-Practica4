from django.db import models
from django.contrib.auth.models import AbstractUser

# Model to stablish the roles of student and teacher to the user extending from AbstractUser wich already gives us the necessary fields
class User(AbstractUser):
    ROLE_STUDENT = 'ST'
    ROLE_TEACHER = 'TE'
    ROLE_CHOICES = [
        (ROLE_STUDENT, 'Student')
        (ROLE_TEACHER, 'Teacher')
    ]

    # we add this field to store the role of the user with the setted up options
    role = models.CharField(max_length=2,choices=ROLE_CHOICES,default=ROLE_STUDENT)

    def is_student(self):
        return self.role == self.ROLE_STUDENT
    def is_teacher(self):
        return self.role == self.ROLE_TEACHER
    
    def __str__(self):
        return self.username