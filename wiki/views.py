from django.db.models import QuerySet
from django.shortcuts import render, redirect
from django.http import HttpResponse, QueryDict
from wiki.models import Article, Section, Category
from wiki.forms import ArticleForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from wiki.models import Article, Section, Category
from wiki.forms import ArticleForm, SectionFormSet


# Create your views here.

def article_list(request, search=""):
    search_prompt = f"{request.GET.get('search_prompt', '')}"
    articles = Article.objects.filter(title__icontains=search_prompt)

    params = {
        "articles": articles,
        "search_prompt": search_prompt,
        "articles_page": True,
    }

    return render(request, "article_list.html", params)

def user_articles(request):

    user = request.user
    if user.is_superuser:
        articles = Article.objects.all()
    else:
        articles = Article.objects.filter(created_by_user=user)

    params = {
        "articles": articles,
    }

    return render(request, "user_articles.html", params)

def article_page(request, i):
    article = Article.objects.get(id=i)
    params = {
        "article": article,
    }
    return render(request, "article_page.html", params)


def new_article(request):
    form = ArticleForm()
    return render(request, "article_edit.html", {"form": form, "sectionset": []})


def article_edit(request, i):
    article = Article.objects.get(id=i)
    form = ArticleForm(instance=article)
    sectionset = SectionFormSet(queryset=article.section_set.all())

    return render(request, "article_edit.html", {"form": form, "sectionset": sectionset})


def article_save(request):
    print("req.post:", request.POST)
    print("request.files:", request.FILES)
    # return redirect(article_list)

    if request.method == "POST":
        print("we gotcha fam")
        post : QueryDict = request.POST
        form = ArticleForm(post)
        if form.is_valid():
            print("valid form")
        art_id = 1
        article = Article.objects.get(id=art_id)
        article.title = post["title"]
        categories = [Category.objects.get(id=cat_id) for cat_id in post.getlist("categories")]
        # article.categories.add(category for category in categories)
        article.short_description = post["short_description"]
        article.main_text = post["main_text"]
        main_img = request.FILES.get("main_image")
        if main_img is not None:
            article.main_image = main_img
        i = 0
        dics = []
        while post.get(str(i)+"_scard_entry_name") is not None:
            dic = {}
            key = post.get(str(i)+"_scard_entry_name")
            values = post.get(str(i)+"_scard_entry_val").split("\r\n")
            dic["name"] = key
            dic["value"] = values
            dics.append(dic)
            i += 1
        article.side_card = dics
        article.save()
        i = 0

        # Apagar sections q ja existem, se n elas vaoficar repetidas
        existing_sections = Section.objects.filter(article_id=art_id)
        for sec in existing_sections:
            sec.delete()
        print("ex:", existing_sections)
        while post.get("form-"+str(i)+"-title") is not None:
            sect = Section(
                article=article,
                position=i,
                title=post["form-"+str(i)+"-title"]
            )
            text = post.get("form-"+str(i)+"-text")
            if text is not None:
                sect.text = text
            img = request.FILES.get("form-"+str(i)+"-image")
            if img is not None:
                sect.image = img
            i += 1
            sect.save()

        print("categories:", categories)


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
    if request.POST:
        action = request.POST['action']
        if action == 'delete_article':
            articleID = request.POST['articleID']
            Article.objects.filter(id=articleID).delete()

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
