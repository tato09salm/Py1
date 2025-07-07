from django import forms
from .models import Categoria, Unidad, Producto, Cliente, Venta

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['descripcion', 'estado']

class UnidadForm(forms.ModelForm):
    class Meta:
        model = Unidad
        fields = ['descripcion', 'estado']
        
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['descripcion', 'categoria', 'estado', 'unidad', 'stock', 'precio']

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['ruc_dni', 'nombres','email','direccion']

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['idcliente', 'fechaventa','idtipo','estado','total','nrodoc','subtotal','igv']