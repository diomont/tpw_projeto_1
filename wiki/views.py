from django.shortcuts import render, redirect
from django.http import HttpResponse
from wiki.models import Article, Section, Category, Subsection
from wiki.forms import ArticleForm


# Create your views here.


def article_list(request):
    search_prompt = f"{request.GET.get('search_prompt', '')}"
    articles = Article.objects.filter(title__icontains=search_prompt)
    # print(articles[0].section_set.all())

    params = {
        "articles": articles,
        "search_prompt": search_prompt,
        "articles_page": True
    }

    return render(request, "article_list.html", params)


def article_page(request, i):
    article = Article.objects.get(id=i)
    print(article.categories)
    params = {
        "article": article
    }
    return render(request, "article_page.html", params)


def article_edit(request, i):
    article = Article.objects.get(id=i)
    form = ArticleForm(instance=article)
    return render(request, "article_edit.html", {"form": form})


def main_page(request):
    return render(request, "main_page.html")

def login(request):
    return render(request, "login.html")

def createAccount(request):
    return render(request, "createAccount.html")

# se DEBUG = False, inserir uma página que não existe irá redirecionar para a página principal
def page_not_found(request, exception):
    return redirect(main_page)