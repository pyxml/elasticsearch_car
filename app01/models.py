from django.db import models


class News(models.Model):

	a_url = models.CharField(max_length=256)
	title = models.CharField(max_length=100)
	desc = models.CharField(max_length=500)
	action_type = models.ForeignKey("Tag",default=0)
	a_uuid = models.CharField(max_length=50,null=True,blank=True)


class Tag(models.Model):

	tag = models.CharField(max_length=25)
