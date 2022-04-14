from django.http import Http404
from django.shortcuts import render , get_list_or_404 , get_object_or_404
from .models import Receitas
from django.db.models import Q
from utils.pagination import make_pagination
import os

PER_PAGE = int(os.environ.get('PER_PAGE',4))

def home(request):

    receitas = Receitas.objects.filter(is_published = True).order_by('-id')

    obj,pagination_range = make_pagination(request,receitas,PER_PAGE)

    return render(request,'receitas/pages/home.html',context={
        'receitas':obj,
        'pagination_range': pagination_range,
    })

def category(request,category_id):
    
    receitas = get_list_or_404(Receitas.objects.filter(category__id = category_id, is_published = True).order_by('-id'))

    obj,pagination_range = make_pagination(request,receitas,PER_PAGE)

    return render(request,'receitas/pages/category.html',context={
        'receitas':obj,
        'pagination_range': pagination_range,
        'title': f"{receitas[0].category.name} - Category"
    })

def receita(request,id):
    
    receita = get_object_or_404(Receitas,is_published = True, pk = id)

    return render(request,'receitas/pages/receita-view.html',context={
        'receita': receita,
        'is_detail_page': True,
    })

def search(request):
   
    search_term = request.GET.get('search','').strip()

    if not search_term:
        raise Http404()

    
    receitas = Receitas.objects.filter(
        Q(Q(title__icontains=search_term) |
        Q(description__icontains=search_term)
        ),
        is_published=True
    ).order_by("-id")

    obj,pagination_range = make_pagination(request,receitas,PER_PAGE)

    return render(request,'receitas/pages/search.html',context={
        'search_title': f'Searching for "{search_term}"',
        'search_term':search_term,
        'receitas': obj,
        'pagination_range': pagination_range,
        'aditional': f'&search={search_term}',
    })