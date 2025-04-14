from django.shortcuts import render
from django.core.cache import cache
from . import terms_work
import re

def index(request):
    return render(request, "index.html")


def terms_list(request):
    terms = terms_work.get_terms_for_table()
    return render(request, "term_list.html", context={"terms": terms})


def add_term(request):
    return render(request, "term_add.html")


def send_term(request):
    if request.method == "POST":
        cache.clear()
        user_name = request.POST.get("name")
        new_term = request.POST.get("new_term", "")
        new_definition = request.POST.get("new_definition", "").replace(";", ",")
        context = {"user": user_name}
        if len(new_definition) == 0:
            context["success"] = False
            context["comment"] = "Описание должно быть не пустым"
        elif len(new_term) == 0:
            context["success"] = False
            context["comment"] = "Термин должен быть не пустым"
        elif bool(re.search(r'[a-zA-Z]', new_term)) or (bool(re.search(r'[a-zA-Z]', new_definition))):
            context["success"] = False
            context["comment"] = "Для иностранных терминов используйте другую форму на нашем сайте"
        else:
            context["success"] = True
            context["comment"] = "Ваш термин принят"
            terms_work.write_term(new_term, new_definition)
        if context["success"]:
            context["success-title"] = ""
        return render(request, "term_request.html", context)
    else:
        add_term(request)


def show_stats(request):
    stats = terms_work.get_terms_stats()
    return render(request, "stats.html", stats)

def add_term_en(request):
    return render(request, "term_add_en.html")

def send_term_en(request):
    if request.method == "POST":
        cache.clear()
        user_name = request.POST.get("name")
        new_term = request.POST.get("new_term", "")
        new_definition = request.POST.get("new_definition", "").replace(";", ",")
        context = {"user": user_name}
        if len(new_definition) == 0:
            context["success"] = False
            context["comment"] = "The description should not be empty"
        elif len(new_term) == 0:
            context["success"] = False
            context["comment"] = "The term should not be empty"
        elif bool(re.search(r'[а-яА-ЯёЁ]', new_term)) or bool(re.search(r'[а-яА-ЯёЁ]', new_definition)):
            context["success"] = False
            context["comment"] = "For Cyrillic terms, use a different form on our website"
        else:
            context["success"] = True
            context["comment"] = "Your term is accepted"
            terms_work.write_term(new_term, new_definition)
        if context["success"]:
            context["success-title"] = ""
        return render(request, "term_request_en.html", context)
    else:
        add_term_en(request)
