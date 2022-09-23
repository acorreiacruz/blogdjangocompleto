from django.urls import path
from . import views

app_name = 'receitas'

urlpatterns = [
    path('',views.ReceitaListViewHome.as_view(),name='home'),
    path('receitas/search/',views.search,name='search'),
    path(
        'receitas/category/<int:category_id>/',
        views.ReceitaListViewCategory.as_view(),
        name='category'
    ),
    path(
        'receitas/<int:id>/',
        views.ReceitaDetailViewReceita.as_view(),
        name='receita'
    ),

]