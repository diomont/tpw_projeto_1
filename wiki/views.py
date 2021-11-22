from django.db.models import QuerySet, ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.http import HttpResponse, QueryDict
from wiki.models import Article, Section, Category
from wiki.forms import ArticleForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, logout
from wiki.models import Article, Section, Category
from wiki.forms import ArticleForm, SectionFormSet


# Create your views here.
def article_list(request, search=""):
    search_prompt = f"{request.GET.get('search_prompt', '')}"
    articles = Article.objects.filter(title__icontains=search_prompt)
    if len(articles) == 0:
        articles = None
    params = {
        "articles": articles,
        "search_prompt": search_prompt,
        "articles_page": True,
    }

    return render(request, "article_list.html", params)


def user_articles(request):
    user = request.user
    if user.is_superuser or user.groups.filter(name='Mods').exists():
        articles = Article.objects.all()
    else:
        articles = Article.objects.filter(created_by_user=user)

    params = {
        "articles": articles,
    }
    return render(request, "user_articles.html", params)


def article_page(request, i):
    if request.POST:
        action = request.POST['action']
        if action == 'delete_article':
            articleID = request.POST['articleID']
            Article.objects.filter(id=articleID).delete()
            return redirect('/articles')

    article = Article.objects.get(id=i)
    isAdmin = request.user.is_superuser
    isMod = request.user.groups.filter(name='Mods').exists()
    isAuthor = (article.created_by_user == request.user)

    params = {
        "article": article,
        "isAdmin": isAdmin,
        "isMod": isMod,
        "isAuthor": isAuthor,
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
    if request.method == "POST":
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
        return False


def main_page(request):
    articles = Article.objects.all()[:5]
    return render(request, "main_page.html", {"articles": articles})


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
        elif action == 'delete_category':
            categoryID = request.POST['categoryID']
            Category.objects.filter(id=categoryID).delete()
        elif action == 'make_mod':
            userID = request.POST['userID']
            users = User.objects.filter(id=userID)
            mods = Group.objects.get(name='Mods')
            for user in users:
                if not user.groups.filter(name='Mods').exists():
                    mods.user_set.add(user)
        elif action == 'unmake_mod':
            userID = request.POST['userID']
            users = User.objects.filter(id=userID)
            mods = Group.objects.get(name='Mods')
            for user in users:
                if user.groups.filter(name='Mods').exists():
                    mods.user_set.remove(user)

    categories = Category.objects.all()
    articles = Article.objects.all()
    sections = Section.objects.all()
    users = User.objects.all()

    params = {
        "categories": categories,
        "articles": articles,
        "sections": sections,
        "users": users,
    }

    return render(request, "admin_page.html", params)


def create_category(request):
    error = False
    just_created_category = False
    if request.POST:
        try:
            name = request.POST['name']
            popularity = int(request.POST['popularity'])
            Category.objects.create(name=name,popularity=popularity)
            just_created_category = True
        except:
            error = True

    params = {
        "error": error,
        "just_created_category": just_created_category,
    }
    return render(request, "category_creation.html", params)


def choose_category(request):
    categories = Category.objects.all()
    params = {
        "categories": categories,
    }
    return render(request, "chooseCategory.html", params)


def category_edit(request, i):
    category = Category.objects.get(id=i)

    error = False
    if request.POST:
        print(request.POST)
        try:
            name = request.POST['name']
            popularity = int(request.POST['popularity'])
            print(category.popularity)
            category.name = name
            category.popularity = popularity
            category.save()
            return redirect('/chooseCategory/')
        except:
            error = True

    params = {
        "category": category,
        "error": error,
    }

    return render(request, "category_edition.html", params)


# se DEBUG = False, inserir uma página que não existe irá redirecionar para a página principal
def page_not_found(request, exception):
    return redirect(main_page)
