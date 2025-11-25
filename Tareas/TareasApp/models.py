from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Model to stablish the roles of student and teacher to the user extending from AbstractUser wich already gives us the necessary fields
class User(AbstractUser):
    ROLE_STUDENT = 'ST'
    ROLE_TEACHER = 'TE'
    ROLE_CHOICES = [
        (ROLE_STUDENT, 'Student'),
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
    
# Model for the groups of users
class Group(models.Model):
    name = models.CharField(max_length=100)
    member = models.ManyToManyField(User,related_name='student_groups')

    def __str__(self):
        return self.name

class Task(models.Model):
    TYPE_INDIVIDUAL = 'IN'
    TYPE_GROUP = 'GR'
    TYPE_EVALUABLE = 'EV'

    TYPE_CHOICES = [
        (TYPE_INDIVIDUAL, 'Individual'),
        (TYPE_GROUP, 'Group'),
        (TYPE_EVALUABLE, 'Evaluable')
    ]

    STATUS_PENDING = 'PE' # Task just created
    STATUS_PENDING_REVIEW = 'PR' # Task pending teacher review
    STATUS_COMPLETED = 'CO' # Task completed
    STATUS_REJECTED = 'RE' # Task evaluation rejected by teacher

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'), 
        (STATUS_PENDING_REVIEW, 'Pending Review'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_REJECTED, 'Rejected')
    ]

    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    task_type = models.CharField(max_length=2,choices=TYPE_CHOICES)
    task_status = models.CharField(max_length=2,choices=STATUS_CHOICES)

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_tasks'
    )

    group = models.ForeignObject(
        Group,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='group_tasks'
    )

    requires_validation = models.BooleanField(default=False)

    is_completed = models.BooleanField(default=False)
    completed_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='completed_tasks'
    )
    completed_at = models.DateTimeField(null=True, blank=True)

    validated_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='validated_tasks'
    )
    validated_at = models.DateTimeField(null=True, blank=True)

    grade = models.DecimalField(max_digits=4,decimal_places=2,null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['task_type']),
            models.Index(fields=['created_by']),
            models.Index(fields=['is_completed']),
        ]
    
    def __str__(self):
        return self.title
    
    