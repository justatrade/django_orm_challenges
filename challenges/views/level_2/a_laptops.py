"""
В этом задании вам предстоит работать с моделью ноутбука. У него есть бренд (один из нескольких вариантов),
год выпуска, количество оперативной памяти, объём жесткого диска, цена, количество этих ноутбуков на складе
и дата добавления.

Ваша задача:
- создать соответствующую модель (в models.py)
- создать и применить миграцию по созданию модели (миграцию нужно добавить в пул-реквест)
- заполнить вашу локальную базу несколькими ноутбуками для облегчения тестирования
  (я бы советовал использовать для этого shell)
- реализовать у модели метод to_json, который будет преобразовывать объект ноутбука в json-сериализуемый словарь
- по очереди реализовать каждую из вьюх в этом файле, проверяя правильность их работу в браузере
"""
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, HttpResponseForbidden
from challenges.models import Laptop


def laptop_details_view(request: HttpRequest, laptop_id: int) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть json-описание ноутбука по его id.
    Если такого id нет, вернуть 404.
    """
    try:
        laptop = Laptop.objects.get(id=laptop_id)
        return HttpResponse(laptop.to_json())
    except Laptop.DoesNotExist:
        return HttpResponseNotFound()


def laptop_in_stock_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть json-описание всех ноутбуков, которых на складе больше нуля.
    Отсортируйте ноутбуки по дате добавления, сначала самый новый.
    """

    laptops = Laptop.objects.filter(quantity__gte=0).order_by('-date_added')
    return HttpResponse('<br>'.join([x.to_json() for x in laptops]))


def laptop_filter_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть список ноутбуков с указанным брендом и указанной минимальной ценой.
    Бренд и цену возьмите из get-параметров с названиями brand и min_price.
    Если бренд не входит в список доступных у вас на сайте или если цена отрицательная, верните 403.
    Отсортируйте ноутбуки по цене, сначала самый дешевый.
    """
    brand = str(request.GET.get('brand', '')).lower()
    min_price = int(request.GET.get('min_price', '0')) if request.GET.get('min_price') else 0
    if min_price < 0 or brand not in list(
            map(
                lambda x: str(x).lower(), set(
                    Laptop.objects.values_list('brand', flat=True)
                )
            )
    ):
        return HttpResponseForbidden()
    laptops = Laptop.objects.filter(brand__iexact=brand, price__gte=min_price)
    return HttpResponse('<br>'.join([laptop.to_json() for laptop in laptops]))


def last_laptop_details_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть json-описание последнего созданного ноутбука.
    Если ноутбуков нет вообще, вернуть 404.
    """
    laptop = Laptop.objects.all().order_by('-date_added').last()
    if laptop:
        return HttpResponse(laptop)
    return HttpResponseForbidden()
