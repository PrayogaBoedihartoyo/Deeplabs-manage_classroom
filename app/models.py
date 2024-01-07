from django.db import models


class Classroom(models.Model):
    teacher = models.CharField(max_length=255)
    student = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.teacher
