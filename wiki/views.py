from django.shortcuts import render, redirect
from django.http import HttpResponse
from wiki.models import Article, Section, Category
from wiki.forms import ArticleForm, SectionFormSet


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
    sectionset = SectionFormSet(queryset=article.section_set.all())

    return render(request, "article_edit.html", {"form": form, "sectionset": sectionset})


def main_page(request):
    return render(request, "main_page.html")


# se DEBUG = False, inserir uma página que não existe irá redirecionar para a página principal
def page_not_found(request, exception):
    return redirect(main_page)