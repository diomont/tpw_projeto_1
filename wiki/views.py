from django.db.models import QuerySet, ObjectDoesNotExist
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
    if request.method == "POST":
        art_id = article_save(request)
        if art_id:
            return redirect("/articles/" + str(art_id))

    form = ArticleForm()
    return render(request, "article_edit.html", {"form": form, "sectionset": []})


def article_edit(request, i):
    if request.method == "POST":
        if article_save(request, i):
            return redirect("/articles/" + str(i))

    article = Article.objects.get(id=i)
    form = ArticleForm(instance=article)
    sectionset = SectionFormSet(queryset=article.section_set.all())

    return render(request, "article_edit.html", {"form": form, "sectionset": sectionset, "id": i})


def article_save(request, art_id=None):
    print("req.post:", request.POST)
    print("request.files:", request.FILES)
    # return redirect(article_list)

    if request.method == "POST":
        # print("we gotcha fam")
        post: QueryDict = request.POST

        if art_id is not None:
            try:
                a = Article.objects.get(id=art_id)
                form = ArticleForm(post, request.FILES, instance=a)
            except Exception:
                form = ArticleForm(post, request.FILES)
        else:
            form = ArticleForm(post, request.FILES)

        if form.is_valid():
            print("valid form")
            inst = form.save()

            for key, val in [(key, val) for key, val in post.items() if "-title" in key]:
                section_number = key.split("-")[1]
                section_name = post.get("form-" + section_number + "-title")
                section_order = int(section_number)
                section_text = post.get("form-" + section_number + "-text")
                section_image = request.FILES.get("form-" + section_number + "-image")
                section_id = post.get("form-" + section_number + "-id")

                if section_id is None:
                    sect = Section(
                            article=inst,
                            position=section_order,
                            title=section_name,
                            text=section_text,
                            image=section_image
                    )
                else:
                    sect = Section.objects.get(id=section_id)
                    sect.position = section_order
                    sect.title = section_name
                    sect.text = section_text
                    if section_image is not None:
                        sect.image = section_image
                sect.save()

            return inst.id

        print(form.errors)

        #     sect = Section(
        #         article=article,
        #         position=i,
        #         title=post["form-"+str(i)+"-title"]
        #     )
        #     text = post.get("form-"+str(i)+"-text")
        #     if text is not None:
        #         sect.text = text
        #     img = request.FILES.get("form-"+str(i)+"-image")
        #     if img is not None:
        #         sect.image = img
        #     i += 1
        #     sect.save()
        #
        # print("categories:", categories)

        return False


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
