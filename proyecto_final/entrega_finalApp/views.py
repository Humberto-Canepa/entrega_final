from django.shortcuts import render
from django.http import HttpResponse
from .forms import *
from .models import *
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test


def Inicio(self):
    
    try:
      avatar = Avatar.objects.get(user=self.user.id)
      return render(self, 'inicio.html', {'url': avatar.imagen.url})
    except:
      return render(self, "inicio.html")


@staff_member_required(login_url='/entrega_finalApp/noaut/')
def Empleado_Formulario(request):
    
    print('method: ', request.method)
    print('post: ', request.POST)

    if request.method == 'POST':
      
      miFormulario = EmpleadoFormulario(request.POST)

      print(miFormulario)

      if miFormulario.is_valid():
          
          data = miFormulario.cleaned_data

          empleado = Empleado(nombre=data['nombre'], apellido=data['apellido'], cargo=data['cargo'])
          empleado.save()
    
          return render(request, "inicio.html")
    
      else:
          
          return render(request, "inicio.html", {"mensaje": "Formulario invalido"})
    
    else:

      miFormulario = EmpleadoFormulario()

      return render(request, "empleado_formulario.html", {"miFormulario": miFormulario})



def Cliente_Formulario(request):
    
    print('method: ', request.method)
    print('post: ', request.POST)

    if request.method == 'POST':
      
      miFormulario = ClienteFormulario(request.POST)

      print(miFormulario)

      if miFormulario.is_valid():
          
          data = miFormulario.cleaned_data

          cliente = Cliente(nombre=data['nombre'], apellido=data['apellido'], email=data['email'])
          cliente.save()
    
          return render(request, "inicio.html")
    
      else:
          
          return render(request, "inicio.html", {"mensaje": "Formulario invalido"})
    
    else:

      miFormulario = ClienteFormulario()

      return render(request, "cliente_formulario.html", {"miFormulario": miFormulario})



def Articulo_Formulario(request):
    
    print('method: ', request.method)
    print('post: ', request.POST)

    if request.method == 'POST':
      
      miFormulario = ArticuloFormulario(request.POST)

      print(miFormulario)

      if miFormulario.is_valid():
          
          data = miFormulario.cleaned_data

          articulo = Tipo_articulo(nombre=data['nombre'], tostado=data['color'], grano=data['dimencion'], cantidad_kg=data['cantidad'])
          articulo.save()
    
          return render(request, "inicio.html")
    
      else:
          
          return render(request, "inicio.html", {"mensaje": "Formulario invalido"})
    
    else:

      miFormulario = ArticuloFormulario()

      return render(request, "articulo_formulario.html", {"miFormulario": miFormulario})



@staff_member_required(login_url='/entrega_finalApp/noaut/')
def Busqueda_Cliente(request):

    return render(request, "busqueda_cliente.html")  

def Buscar(request):
  
    if request.GET["nombre"]:
        
        nombre = request.GET["nombre"]
        cliente = Cliente.objects.filter(nombre=nombre)
        return render(request, "resultados_busqueda.html", {"cliente": cliente, "nombre": nombre})
    
    else:
        return HttpResponse(f'No se recibio informacion')



class Lista_articulo(LoginRequiredMixin, ListView):
  
  model = Tipo_articulo
  template_name = 'lista_articulo.html'
  context_object_name = 'articulo'

class Articulo_detail(DetailView):
  
  model = Tipo_articulo
  template_name = 'articulo_detail.html'
  context_object_name = 'articulo_det'



class Articulo_Create(CreateView):
   
  model = Tipo_articulo
  template_name = 'articulo_create.html'
  fields = ['nombre', 'color', 'dimencion', 'cantidad', 'imagen']
  success_url = '/entrega_finalApp/'

  def form_valid(self, form):
    response = super().form_valid(form)
    if 'imagen' in self.request.FILES:
      self.object.imagen = self.request.FILES['imagen']
      self.object.save()
    return response



class Articulo_Update(UpdateView):
    model = Tipo_articulo
    template_name = 'articulo_update.html'
    fields = ['nombre', 'color', 'dimencion', 'cantidad', 'imagen']
    success_url = '/entrega_finalApp/'
    context_object_name = 'articulo_up'

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.FILES.get('imagen'):
            self.object.imagen = self.request.FILES['imagen']
            self.object.save()
        return response



class Articulo_Delete(DeleteView):
   
   model = Tipo_articulo
   template_name = 'articulo_delete.html'
   success_url = '/entrega_finalApp/'



def loginV(request):
   
  if request.method == 'POST':
    miform = AuthenticationForm(request, data=request.POST)

    if miform.is_valid():
        
      data = miform.cleaned_data
      usuario = data["username"]
      psw = data["password"]
      
      user = authenticate(username=usuario, password=psw)

      if user:
        login(request, user)
        return render(request, 'inicio.html', {"mensaje": f'Bienvenido {usuario}'})
      
      else:
        return render(request, 'inicio.html', {"mensaje": f'Formulario invalido'})
         
    else:
      return render(request, "inicio.html", {"mensaje": "Usuario o contraseña inexistente!"})
  else:
    miform = AuthenticationForm()
    return render(request, "login.html", {"miform": miform})



def Register(request):
   
  if request.method == 'POST':
    miform = UserCreationForm(request.POST)

    if miform.is_valid():
        
      data = miform.cleaned_data
      username = data["username"]
      miform.save()
      return render(request, 'inicio.html', {"mensaje": f'Usuario {username} creado!'})
         
    else:
      return render(request, "inicio.html", {"mensaje": "Formulario invalido"})
  
  else:
    miform = UserCreationForm()
    return render(request, "registro.html", {"miform": miform})  
  


@login_required
def Editar_Perfil(request):

    usuario = request.user

    if request.method == 'POST':
      
      miform = UserEditForm(request.POST, instance=request.user)

      if miform.is_valid():
          data = miform.cleaned_data

          usuario.first_name = data['first_name']
          usuario.last_name = data['last_name']
          usuario.email = data['email']
          usuario.set_password(data["password1"])
          usuario.save()
          
          return render(request, "inicio.html", {"mensaje": "Datos actualizados, vuelve a iniciar sesion"})
    
      else:
          return render(request, "inicio.html", {"miform": miform})
    else:
      miform = UserEditForm(instance=request.user)
      return render(request, "editar_perfil.html", {"miform": miform})



def About(request):
    context = {
        'title': 'Acerca de mí',
        'image_url': '/media/avatares/perfil.jpg',
        'texto': """Mi nombre es Humberto Cánepa.
Soy Argentino y actualmente me encuentro viviendo en la ciudad de Salta.
Estudie Ingenieria Industrial y actualmente me encuentro inspeccionando el rubro de la informatica.
Siempre quise empezar a instruirme en dicho rubro ya que considero que es una gran herramienta para cualquier trabajo, por lo que me encuentro 
finalizando el curso de Python en CoderHouse. 
""",
    }
    return render(request, 'about.html', context)



def Noaut(request):
   return render(request, "noaut.html")
