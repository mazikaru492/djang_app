from django import forms

from .models import Book


class BookForm(forms.ModelForm):
	class Meta:
		model = Book
		fields = ["title", "author", "price", "genre", "description", "pub_date"]
		labels = {
			"pub_date": "出版日",
		}
		widgets = {
			"pub_date": forms.DateInput(attrs={"type": "date"}),
		}
