from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BookForm
from .models import Book


def index(request):
	q = request.GET.get("q", "")
	books = Book.objects.select_related("genre").all().order_by("-pub_date")
	if q:
		books = books.filter(title__icontains=q)
	page = Paginator(books, 5).get_page(request.GET.get("page"))
	return render(request, "book/itiran.html", {"page": page, "q": q})


def book_detail(request, pk):
	book = get_object_or_404(Book.objects.select_related("genre"), pk=pk)
	return render(request, "book/syousai.html", {"book": book})


def book_create(request):
	if request.method == "POST":
		form = BookForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect("index")
	else:
		form = BookForm()
	return render(request, "book/form.html", {"form": form, "mode": "新規登録"})


def book_update(request, pk):
	book = get_object_or_404(Book, pk=pk)
	if request.method == "POST":
		form = BookForm(request.POST, instance=book)
		if form.is_valid():
			form.save()
			return redirect("index")
	else:
		form = BookForm(instance=book)
	return render(request, "book/form.html", {"form": form, "mode": "編集"})


def book_delete(request, pk):
	book = get_object_or_404(Book, pk=pk)
	if request.method == "POST":
		book.delete()
		return redirect("index")
	return render(request, "book/confirm.html", {"book": book})
