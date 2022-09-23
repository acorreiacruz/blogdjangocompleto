from django.views.generic import ListView, DetailView
from django.views import View
from django.http import Http404
from django.shortcuts import render , get_list_or_404 , get_object_or_404
from .models import Receitas
from django.db.models import Q
from utils.pagination import make_pagination
import os

PER_PAGE = int(os.environ.get('PER_PAGE',4))


class ReceitaListViewBase(ListView):
    model = Receitas
    context_object_name = 'receitas'
    ordering = ['-id']
    template_name = 'receitas/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        obj, pagination_range = make_pagination(self.request, self.get_queryset(), PER_PAGE)
        context.update({
            'receitas': obj,
            'pagination_range': pagination_range
        })
        return context


class ReceitaListViewHome(ReceitaListViewBase):
    model = Receitas
    context_object_name = 'receitas'
    template_name = 'receitas/pages/home.html'


class ReceitaListViewCategory(ReceitaListViewBase):
    model = Receitas
    context_object_name = 'receitas'
    template_name = 'receitas/pages/category.html'

    def get_queryset(self, *args, **kwargs):
        receitas = get_list_or_404(
            Receitas.objects.all(),
            is_published=True,
            category__id=self.kwargs.get('category_id')
        )
        return receitas

    def get_context_data(self, *args, **kwargs):
        first = self.get_queryset()[0]
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'title': f'{first.category.name} - Category'
        })
        return context


class ReceitaDetailViewReceita(DetailView):
    model = Receitas
    context_object_name = 'receita'
    template_name = 'receitas/pages/receita-view.html'

    def get_object(self, *args, **kwargs):
        obj = get_object_or_404(
            Receitas.objects.all(),
            is_published=True,
            id=self.kwargs.get('id')
        )
        return obj

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'is_detail_page': True
        })
        return context


class ReceitaViewSearch(View):

    def get(self, request):
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