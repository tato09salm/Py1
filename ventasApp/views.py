from django.shortcuts import render, redirect, get_object_or_404
from .models import Categoria
from .forms import CategoriaForm
from .models import Unidad
from .forms import UnidadForm
from .models import Producto
from .forms import ProductoForm

from .models import Cliente
from .forms import ClienteForm

from .models import Venta
from .forms import VentaForm
from django.contrib import messages

from django.http import JsonResponse

##venta###
from django.utils import timezone
from django.shortcuts import render, redirect
from .models import Cliente, Producto, Tipo, Parametro
from django.http import JsonResponse

from django.db.models import Q


from .models import Venta, DetalleVenta
from django.db import transaction
from django.utils.dateparse import parse_date


def listarcategoria(request):
    queryset = request.GET.get("buscar")
    categoria = Categoria.objects.filter(estado=True)
    if queryset:
        categoria = Categoria.objects.filter(
            Q(descripcion__icontains=queryset), estado=True
        ).distinct()
    context = {'categoria': categoria}
    return render(request, "categoria/listar.html", context)

def agregarcategoria(request):
    if request.method == "POST":
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("listarcategoria")
    else:
        form = CategoriaForm()
    return render(request, "categoria/agregar.html", {'form': form})

def editarcategoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    if request.method == "POST":
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect("listarcategoria")
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, "categoria/editar.html", {'form': form})

def eliminarcategoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    categoria.estado = False
    categoria.save()
    return redirect("listarcategoria")

def listar_unidades(request):
    queryset = request.GET.get("buscar")
    unidades = Unidad.objects.filter(estado=True)
    if queryset:
        unidades = Unidad.objects.filter(
            descripcion__icontains=queryset, estado=True
        ).distinct()
    context = {'unidades': unidades}
    return render(request, "unidad/listar.html", context)

def agregar_unidad(request):
    if request.method == "POST":
        form = UnidadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("listar_unidades")
    else:
        form = UnidadForm()
    return render(request, "unidad/agregar.html", {'form': form})

def editar_unidad(request, id):
    unidad = get_object_or_404(Unidad, id=id)
    if request.method == "POST":
        form = UnidadForm(request.POST, instance=unidad)
        if form.is_valid():
            form.save()
            return redirect("listar_unidades")
    else:
        form = UnidadForm(instance=unidad)
    return render(request, "unidad/editar.html", {'form': form})

def eliminar_unidad(request, id):
    unidad = get_object_or_404(Unidad, id=id)
    unidad.estado = False
    unidad.save()
    return redirect("listar_unidades")

def listar_productos(request):
    productos = Producto.objects.all()
    context = {'productos': productos}
    return render(request, "producto/listar.html", context)

def agregar_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = ProductoForm()
    return render(request, "producto/agregar.html", {'form': form})

def editar_producto(request, id):
    producto = get_object_or_404(Producto, producto_id=id)
    if request.method == "POST":
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, "producto/editar.html", {'form': form})

def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, producto_id=id)
    producto.delete()
    return redirect('listar_productos')

def listarcliente(request):
    queryset = request.GET.get("buscar")
    if queryset:
        cliente = Cliente.objects.filter(
            Q(nombres__icontains=queryset) |
            Q(dni__icontains=queryset) |
            Q(codigo__icontains=queryset)
        ).distinct()
    else:
        cliente = Cliente.objects.all()
    context = {'cliente': cliente}
    return render(request, "cliente/listar.html", context)

def agregarcliente(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("listarcliente")
    else:
        form = ClienteForm()
    return render(request, "cliente/agregar.html", {'form': form})

def editarcliente(request, id):
    cliente = get_object_or_404(Cliente, idcliente=id)
    if request.method == "POST":
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect("listarcliente")
    else:
        form = ClienteForm(instance=cliente)
    return render(request, "cliente/editar.html", {'form': form})

def eliminarcliente(request, id):
    cliente = get_object_or_404(Cliente, idcliente=id)
    cliente.delete()  # eliminación física
    return redirect("listarcliente")



#####VENTA############
from django.db.models import Q

def listarventa(request):
    buscar = request.GET.get('buscarpor', '').strip()
    
    # Obtener estado de los parámetros GET; por defecto 1
    estado = request.GET.get('estado', '1')
    
    # Validar que estado sea un número entero
    try:
        estado = int(estado)
    except ValueError:
        estado = 1  # valor por defecto si el parámetro no es válido

    # Filtrar ventas por estado
    ventas = Venta.objects.filter(estado=estado).order_by('-fechaventa')
    no_resultado = False

    if buscar:
        palabras = buscar.split()
        filtro = Q()
        for palabra in palabras:
            filtro &= Q(idcliente__nombres__icontains=palabra)
        
        ventas = ventas.filter(filtro)
        no_resultado = not ventas.exists()

    return render(request, 'venta/listar.html', {
        'ventas': ventas,
        'buscarpor': buscar,
        'estado': estado,
        'no_resultado': no_resultado,
    })


def agregarventa(request):
    if request.method == 'POST':
        try:
            # Crear venta
            venta = Venta()
            venta.fechaventa = timezone.datetime.strptime(request.POST.get('fechaventa'), "%d/%m/%Y").date()
            venta.nrodoc = request.POST.get('nrodoc')
            venta.subtotal = float(request.POST.get('subtotal'))
            venta.igv = float(request.POST.get('igv'))
            venta.total = float(request.POST.get('total'))
            venta.estado = 1
            venta.idcliente_id = int(request.POST.get('idcliente'))
            venta.idtipo_id = int(request.POST.get('idtipo'))
            venta.save()

            # Guardar detalles
            idproductos = request.POST.getlist('idproducto[]')
            cantidades = request.POST.getlist('cantidad[]')
            precios = request.POST.getlist('pventa[]')

            for i in range(len(idproductos)):
                detalle = DetalleVenta()
                detalle.idventa_id = venta.id  # asigna la venta recién guardada
                detalle.idproducto_id = int(idproductos[i])
                detalle.cantidad = float(cantidades[i])
                detalle.precio = float(precios[i])
                detalle.save()

            return redirect('listarventa')
        
            #return redirect('listarventa', id=venta.id)
        except Exception as e:
            print("Error al guardar venta:", e)
            # Podrías mostrar un mensaje en la plantilla con un contexto si deseas
            return render(request, 'venta/agregar.html', {
                'error': 'Error al guardar venta',
                "tipos": Tipo.objects.all(),
                "clientes": Cliente.objects.all(),
                "productos": Producto.objects.all(),
                "fecha_actual": timezone.now().strftime("%d/%m/%Y"),
                "parametros": {},
            })

    # Si GET
    return render(request, 'venta/agregar.html', {
        "tipos": Tipo.objects.all(),
        "clientes": Cliente.objects.all(),
        "productos": Producto.objects.all(),
        "fecha_actual": timezone.now().strftime("%d/%m/%Y"),
        "parametros": {},  # puedes cambiarlo si usas un objeto para numeración
    })

def editarcliente(request, id):
    cliente = get_object_or_404(Cliente, idcliente=id)
    if request.method == "POST":
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect("listarcliente")
    else:
        form = ClienteForm(instance=cliente)
    return render(request, "cliente/editar.html", {'form': form})

def eliminarcliente(request, id):
    cliente = get_object_or_404(Cliente, idcliente=id)
    cliente.delete()  # eliminación física
    return redirect("listarcliente")


def obtener_parametro_por_tipo(request, id):
    try:
        parametro = Parametro.objects.get(idtipo=id)
        return JsonResponse({'nrodoc': parametro.numeracion})
    except Parametro.DoesNotExist:
        return JsonResponse({'nrodoc': ''})
    

##autocompletar
def obtener_datos_cliente(request, idcliente):
    try:
        cliente = Cliente.objects.get(pk=idcliente)
        return JsonResponse({
            'ruc_dni': cliente.ruc_dni,
            'direccion': cliente.direccion
        })
    except Cliente.DoesNotExist:
        return JsonResponse({}, status=404)

def obtener_datos_producto(request, producto_id):
    try:
        producto = Producto.objects.get(pk=producto_id)
        return JsonResponse({
            'precio': producto.precio,
            'stock': producto.stock,
            'unidad': producto.unidad.descripcion
        })
    except Producto.DoesNotExist:
        return JsonResponse({}, status=404)

def anular_venta(request, id):
    venta = get_object_or_404(Venta, id=id)
    
    # Puedes hacer algo como marcarla como anulada:
    venta.estado = '0'  # Asume que tienes un campo 'estado'
    venta.save()
    
    messages.success(request, f"La venta #{id} fue anulada exitosamente.")
    return redirect('listarventa')