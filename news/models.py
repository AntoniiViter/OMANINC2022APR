from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=100)
    info = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datearchived = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(upload_to='news/images/', blank=True)
    url = models.URLField(blank=True)
    newscreator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "%s (%s) [%s]" % (self.title, self.pk, self.newscreator)
