from django.shortcuts import render, redirect
from django.http import HttpResponse
from wiki.models import Article, Section, Category
from wiki.forms import ArticleForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
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
    params = {
        "article": article,
    }
    return render(request, "article_page.html", params)


def article_edit(request, i):
    article = Article.objects.get(id=i)
    form = ArticleForm(instance=article)
    sectionset = SectionFormSet(queryset=article.section_set.all())

    return render(request, "article_edit.html", {"form": form, "sectionset": sectionset})


def article_save(request):

    if request.method == "POST":
        print("we gotcha fam")
    print("req:", request)
    print("req.post:", request.POST)

    return redirect(article_list)


def main_page(request):
    return render(request, "main_page.html")


def createAccount(request):
    if request.POST:
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        user = User.objects.create_user(username, email, password)
        user.first_name = firstname
        user.last_name = lastname

        user.save()
        return redirect('/login')

    else:
        return render(request, "createAccount.html")


def profile(request):
    params = {
        "profile_page": True,
    }
    return render(request, "profilePage.html", params)


def logout_view(request):
    logout(request)
    return redirect('/')


def change_password(request):
    if request.POST:
        new_password = request.POST['new_password']
        new_password_conf = request.POST['new_password_conf']

        if new_password==new_password_conf:
            user = request.user
            user.set_password(new_password)
            user.save()
            return redirect('/login')
        else:
            params = {"error": True}
            return render(request, "changePassword.html", params)
    else:
        params = {"error": False}
        return render(request, "changePassword.html", params)

def adminPage(request):
    categories = Category.objects.all()
    articles = Article.objects.all()
    sections = Section.objects.all()

    params = {
        "categories": categories,
        "articles": articles,
        "sections": sections,
    }

    return render(request, "admin_page.html", params)


# se DEBUG = False, inserir uma página que não existe irá redirecionar para a página principal
def page_not_found(request, exception):
    return redirect(main_page)
