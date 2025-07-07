from django.db import models
from django.utils import timezone

class Categoria(models.Model):
    descripcion = models.CharField(max_length=30)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.descripcion

class Unidad(models.Model):
    descripcion = models.CharField(max_length=30)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.descripcion

class Producto(models.Model):
    producto_id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=40)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    estado = models.CharField(max_length=1)
    unidad = models.ForeignKey(Unidad, on_delete=models.CASCADE)
    stock = models.FloatField()
    precio = models.FloatField()

    def __str__(self):
        return self.descripcion

class Cliente(models.Model):
    idcliente =  models.AutoField(primary_key=True)
    ruc_dni= models.CharField(max_length=11)
    nombres = models.CharField(max_length=80)
    email = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)

    class Meta:
        db_table = 'clientes'
        managed = False  

    def __str__(self):
        return self.nombres 

class Tipo(models.Model):
    descripcion = models.CharField(max_length=50)

    class Meta:
        db_table = 'tipo'
        managed = False  

    def __str__(self):
        return self.descripcion

class Venta(models.Model):
    idcliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, db_column='idcliente')
    fechaventa = models.DateField(default=timezone.now)
    idtipo = models.ForeignKey(Tipo, on_delete=models.PROTECT, db_column='idtipo')
    estado = models.IntegerField(default=1)
    total = models.FloatField(default=0)
    nrodoc = models.CharField(max_length=12)
    subtotal = models.FloatField(default=0)
    igv = models.FloatField(default=0)

    class Meta:
        db_table = 'cabeceraventa'
        managed = False  

    def __str__(self):
        return f'Venta {self.id} — {self.nrodoc}'

class DetalleVenta(models.Model):
    idventa = models.ForeignKey(Venta, on_delete=models.CASCADE, db_column='idventa')
    idproducto = models.ForeignKey(Producto, on_delete=models.PROTECT, db_column='idproducto')
    precio = models.FloatField(default=0)
    cantidad = models.FloatField(default=0)

    class Meta:
        db_table = 'detalleventa'
        managed = False  

    def __str__(self):
        return f'Detalle Venta {self.idventa.id}'

class Parametro(models.Model):
    idtipo =  models.AutoField(primary_key=True)
    numeracion = models.CharField(max_length=15)
    serie = models.CharField(max_length=3)

    class Meta:
        db_table = 'parametros'
        managed = False  

    def __str__(self):
        return self.numeracion



