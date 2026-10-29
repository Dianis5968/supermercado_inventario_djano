from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Producto
from .forms import ProductoForm

# 🔹 VISTA 1: LISTAR PRODUCTOS (con paginación que él muestra)
def lista_productos(request):
    # Paso 1: Traer TODOS los productos de la base de datos
    qs = Producto.objects.all()
    # Paso 2: Dividir la lista en páginas (10 productos por página)
    paginator = Paginator(qs, 10)
    # Paso 3: Saber qué número de página mostrar
    pagina = request.GET.get('page',1)
    # Paso 4: Obtener solo los productos de esa página
    productos = paginator.get_page(pagina)
    # Paso 5: Enviar esos productos a la plantilla HTML para mostrarlos
    return render(request, 'inventario/lista_productos.html', {'productos': productos})

# 🔹 VISTA 2: CREAR PRODUCTO (AQUÍ ESTÁ EL GET / POST QUE PIDE LA EVIDENCIA)
def crear_producto(request):
    # ✅ CASO POST: el usuario YA llenó el formulario y pulsó GUARDAR
    if request.method == 'POST':
        # Creamos el formulario con los datos que envió el usuario
        form = ProductoForm(request.POST)
        # Verificamos que todos los datos estén correctos
        if form.is_valid():
            # Guardamos en la base de datos
            form.save()
            # Volvemos a la lista de productos
            return redirect('inventario:lista')
    # ✅ CASO GET: el usuario SOLO entró a la página para VER el formulario vacío
    else:
        # Creamos un formulario VACÍO para que el usuario llene
        form = ProductoForm()
    # Enviamos el formulario a la página HTML
    return render(request, 'inventario/formulario_producto.html', {'form': form})

# 🔹 VISTA 3: EDITAR PRODUCTO (también GET / POST + pk)
def editar_producto(request, pk):
    # Paso 1: Buscar el producto por su ID (pk = primary key)
    producto = get_object_or_404(Producto, pk=pk)
    # ✅ CASO POST: el usuario ya modificó y pulsó guardar
    if request.method == 'POST':
        # Cargamos el formulario con los datos NUEVOS y el producto existente
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('inventario:lista')
    # ✅ CASO GET: el usuario solo entró para VER los datos que ya tiene el producto
    else:
        # Cargamos el formulario con los datos antiguos del producto
        form = ProductoForm(instance=producto)
    return render(request, 'inventario/formulario_producto.html', {'form': form})

# 🔹 VISTA 4: ELIMINAR PRODUCTO (GET = ver confirmación / POST = borrar)
def eliminar_producto(request, pk):
    # Paso 1: Buscar el producto que queremos borrar
    producto = get_object_or_404(Producto, pk=pk)
    # ✅ CASO POST: el usuario confirmó que SÍ quiere borrar
    if request.method == 'POST':
        producto.delete()
        return redirect('inventario:lista')
    # ✅ CASO GET: el usuario solo entró para VER la pregunta de confirmación
    else:
        return render(request, 'inventario/confirmar_eliminar.html', {'producto': producto})