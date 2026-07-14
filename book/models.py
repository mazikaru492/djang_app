from django.db import models


class Genre(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name


class Book(models.Model):
	title = models.CharField(max_length=100)
	author = models.CharField(max_length=50)
	price = models.IntegerField()
	genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
	description = models.TextField()
	pub_date = models.DateField(verbose_name="出版日")

	def __str__(self):
		return self.title
