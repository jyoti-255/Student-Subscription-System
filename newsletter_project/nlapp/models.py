from django.db import models

class StudentModel(models.Model):
    phone = models.CharField(max_length=15, primary_key=True)
    crdt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone
