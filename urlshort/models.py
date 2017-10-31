from django.db import models
from django.conf import settings

class Sam(models.Model):
	user=models.ForeignKey(settings.AUTH_USER_MODEL, null=True,blank=True)
	originalurl = models.CharField(max_length=1000)
	shorten =models.CharField(max_length=500)
	clicks = models.CharField(max_length=500,default=0)

	def __str__(self):
		return self.shorten +self.clicks
