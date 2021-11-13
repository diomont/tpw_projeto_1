from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.


def article_list(request):
    search_prompt = f"{request.GET.get('search_prompt', '')}"

    params = {
        "articles": [
            {
                "category": {
                    "name": "Estudo Científico",
                },
                "title": "Top 10 dias da semana",
                "main_image": "https://st3.depositphotos.com/1954927/13199/v/450/depositphotos_131991952-stock-illustration-november-15-calendar-icon-vector.jpg",
                "short_description": "Um Top 10 essencial para o uso!"
            },
            {
                "category": {
                    "name": "Estudo Científico",
                },
                "title": "Como sobreviver a LEI: Curso Intensivo",
                "main_image": "https://thumbs.dreamstime.com/b/tired-worker-typing-keyboard-selective-focus-man-head-29791502.jpg",
                "short_description": "Spoilers: u fucked m8"
            }
        ],
        "search_prompt": search_prompt
    }

    return render(request, "article_list.html", params)


def article_page(request):
    return render(request, "article_page.html")


def main_page(request):
    return render(request, "main_page.html")
