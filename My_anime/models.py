from django.db import models
from django.utils import timezone
from django.urls import reverse
from Films.models import Film
# Create your models here.
class My_List(models.Model):
    status_choices = (
        ('watch list', 'WATCH LIST'),
        ('complete', 'COMPLETE'),
        ('watching', 'watching')
    )
    status = models.TextField(max_length=100, choices=status_choices)
    current = models.IntegerField()
    Local = models.TextField(max_length=200)
    List = models.ForeignKey(Film, on_delete=models.CASCADE)
    registered =  models.DateTimeField(default = timezone.now)
    updated = models.DateTimeField(auto_now=True)

    def absolute_url(self):
        return reverse('My_anime:my_list_detail', args=[self.status, self.registered.year, self.registered.month, self.registered.day])




