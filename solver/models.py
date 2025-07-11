from django.db import models
from django.contrib.auth.models import User

class All_account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=12)
    address = models.TextField()
    
    STANDARD_CHOICES = [
        ('1', 'Class 1'),
        ('2', 'Class 2'),
        ('3', 'Class 3'),
        ('4', 'Class 4'),
        ('5', 'Class 5'),
        ('6', 'Class 6'),
        ('7', 'Class 7'),
        ('8', 'Class 8'),
        ('9', 'Class 9'),
        ('10', 'Class 10'),
        ('11', 'Class 11'),
        ('12', 'Class 12'),
    ]
    standard = models.CharField(max_length=2, choices=STANDARD_CHOICES)

    def __str__(self):
        return self.user.username
    
    
class Problem(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    options = models.JSONField()  # ["A", "B", "C", "D"]
    correct_option = models.IntegerField()  # index of correct option
    standard = models.IntegerField(default=None)
    

    def __str__(self):
        return self.title

class UserProblemStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    is_solved = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'problem')
