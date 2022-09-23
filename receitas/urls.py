from django.urls import path
from . import views

app_name = 'receitas'

urlpatterns = [
    path('',views.ReceitaListViewBase.as_view(),name='home'),
    path('receitas/search/',views.search,name='search'),
    path('receitas/category/<int:category_id>/',views.category,name='category'),
    path('receitas/<int:id>/',views.receita,name='receita'),

]