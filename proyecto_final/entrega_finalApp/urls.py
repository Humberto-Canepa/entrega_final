from django.contrib import admin
from django.urls import path
from entrega_finalApp.views import *
from django.contrib.auth.views import LogoutView
from django.contrib.admin.views.decorators import staff_member_required

urlpatterns = [
   path('', Inicio, name="inicio"),
   path('empleado-formulario/', Empleado_Formulario, name="empleado_formulario"),
   path('cliente-formulario/', Cliente_Formulario, name="cliente_formulario"),
   path('articulo-formulario/', Articulo_Formulario, name="articulo_formulario"),
   path('busqueda-cliente/', Busqueda_Cliente, name="busqueda_cliente"),
   path('buscar/', Buscar, name="resultados_busqueda"),
   path('lista-articulos/', staff_member_required(Lista_articulo.as_view(), redirect_field_name='/entrega_finalApp/noaut/'), name="lista_articulos"),
   path('articulo-detail/<pk>/', Articulo_detail.as_view(), name="articulo_detail"),
   path('articulo-create/', Articulo_Create.as_view(), name="articulo_create"),
   path('articulo-update/<pk>/', Articulo_Update.as_view(), name="articulo_update"),
   path('articulo-delete/<pk>/', Articulo_Delete.as_view(), name="articulo_delete"),
   path('login/', loginV, name="login"),
   path('registro/', Register, name="registro"),
   path('logout/', LogoutView.as_view(template_name='logout.html'), name="logout"),
   path('editar-perfil/', Editar_Perfil, name="editar_perfil"),
   path('about/', About, name='about'),
   path('noaut/', Noaut, name="noaut"),

]