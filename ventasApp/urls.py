from django.urls import path,include
from .views import listarcategoria, agregarcategoria, editarcategoria, eliminarcategoria
from .views import listar_unidades, agregar_unidad, editar_unidad, eliminar_unidad
from .views import listar_productos, agregar_producto, editar_producto, eliminar_producto

from .views import listarcliente, agregarcliente, editarcliente, eliminarcliente
from .views import listarventa, agregarventa
from django.contrib.auth import views
from ventasApp import views  
urlpatterns = [
    path('listacategoria/', listarcategoria, name="listarcategoria"),
    path('agregarcategoria/', agregarcategoria, name="agregarcategoria"),
    path('editarcategoria/<int:id>/', editarcategoria, name="editarcategoria"),
    path('eliminarcategoria/<int:id>/', eliminarcategoria, name="eliminarcategoria"),
    path('listar_unidades/', listar_unidades, name="listar_unidades"),
    path('agregar_unidad/', agregar_unidad, name="agregar_unidad"),
    path('editar_unidad/<int:id>/', editar_unidad, name="editar_unidad"),
    path('eliminar_unidad/<int:id>/', eliminar_unidad, name="eliminar_unidad"),
    path('listar_productos/', listar_productos, name='listar_productos'),
    path('agregar_producto/', agregar_producto, name='agregar_producto'),
    path('editar_producto/<int:id>/', editar_producto, name='editar_producto'),
    path('eliminar_producto/<int:id>/', eliminar_producto, name='eliminar_producto'),

    path('listacliente/', listarcliente, name="listarcliente"),
    path('agregarcliente/', agregarcliente, name="agregarcliente"),
    path('editarcliente/<int:id>/', editarcliente, name="editarcliente"),
    path('eliminarcliente/<int:id>/', eliminarcliente, name="eliminarcliente"),

    path('listaventa/', listarventa, name="listarventa"),
    path('agregarventa/', agregarventa, name="agregarventa"),
    

    path('venta/parametro-por-tipo/<int:id>/', views.obtener_parametro_por_tipo, name='obtener_parametro'),

    ##autompletado
    path('venta/datos-cliente/<int:idcliente>/', views.obtener_datos_cliente, name='datos_cliente'),
    path('venta/datos-producto/<int:producto_id>/', views.obtener_datos_producto, name='datos_producto'),

    #path('venta/agregar/', views.agregar_venta, name='agregarventa'),


    #path('detalleventa/<int:id>/', views.detalle_venta, name='detalleventa'),
    path('listaventa/', listarventa, name="listarventa"),
    path('venta/anular/<int:id>/', views.anular_venta, name='anular_venta'),

]
