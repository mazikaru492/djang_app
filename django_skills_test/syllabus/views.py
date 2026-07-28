from django.core.paginator import Paginator
from django.shortcuts import render


def index(request):
	data = [
		{"id": 1, "name": "Alice", "age": 20, "mail": "alice@example.com", "birthday": "2006-01-01"},
		{"id": 2, "name": "Bob", "age": 21, "mail": "bob@example.com", "birthday": "2005-02-02"},
		{"id": 3, "name": "Carol", "age": 22, "mail": "carol@example.com", "birthday": "2004-03-03"},
	]
	paginator = Paginator(data, 2)
	page_number = request.GET.get("page")
	page_obj = paginator.get_page(page_number)
	context = {
		"title": "syllabus index",
		"message": "syllabus app is ready.",
		"data": page_obj,
	}
	return render(request, "django_skills_test/index.html", context)


