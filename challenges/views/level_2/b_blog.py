"""
В этом задании вам предстоит работать с моделью поста в блоге. У него есть название, текст, имя автора, статус
(опубликован/не опубликован/забанен), дата создания, дата публикации, категория (одна из нескольких вариантов).

Ваша задача:
- создать соответствующую модель (в models.py)
- создать и применить миграцию по созданию модели (миграцию нужно добавить в пул-реквест)
- заполнить вашу локальную базу несколькими ноутбуками для облегчения тестирования
- реализовать у модели метод to_json, который будет преобразовывать объект книги в json-сериализуемый словарь
- по очереди реализовать каждую из вьюх в этом файле, проверяя правильность их работу в браузере
"""
import datetime

from django.http import HttpRequest, HttpResponse
from django.db.models import Q

from challenges.models import Post


def last_posts_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть 3 последних опубликованных поста.
    """
    # Post.objects.create(title='Some tweet 3',
    #                     text='It\'s not even a second tweet',
    #                     author_name='Ilon Musk clone',
    #                     status='posted',
    #                     category='news')
    # post = Post.objects.get(id=4)
    posts = Post.objects.filter(status='posted').order_by('-date_posted')[:3]
    return HttpResponse('<br>'.join([post.to_json() for post in posts]))


def posts_search_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть все посты, которые подходят под поисковый запрос.
    Сам запрос возьмите из get-параметра query.
    Подходящесть поста можете определять по вхождению запроса в название или текст поста, например.
    """
    query = request.GET.get('query')
    posts = []
    if query:
        status = 200
        posts = Post.objects.filter(Q(text__icontains=query) | Q(title__icontains=query))
    else:
        status = 404
    return HttpResponse('<br>'.join([str(_) for _ in posts]), status=status)


def untagged_posts_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть все посты без категории, отсортируйте их по автору и дате создания.
    """
    posts = Post.objects.filter(category__isnull=True).order_by('author_name', 'date_created')
    return HttpResponse('<br>'.join([str(_) for _ in posts]))


def categories_posts_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть все посты все посты, категория которых принадлежит одной из указанных.
    Возьмите get-параметр categories, в нём разделённый запятой список выбранных категорий.
    """
    categories = request.GET.get('categories').split(',')
    posts = Post.objects.filter(category__in=categories)
    return HttpResponse('<br>'.join([str(_) for _ in posts]))


def last_days_posts_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть посты, опубликованные за последние last_days дней.
    Значение last_days возьмите из соответствующего get-параметра.
    """
    last_days = int(request.GET.get('last_days'))
    time_delta = datetime.datetime.now() - datetime.timedelta(days=last_days)
    posts = Post.objects.filter(
        status='posted',
        date_posted__gte=time_delta)
    return HttpResponse('<br>'.join([str(_) for _ in posts]))
