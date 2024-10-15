from django.urls import path
from reservas import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('reservar_servicio/', views.reservar_servicio, name='reservar_servicio'),
    
    path('api/razas/', views.obtener_razas, name='obtener_razas'),
    path('api/servicios/', views.obtener_servicios, name='obtener_servicios'),
    path('crear-reserva/', views.crear_reserva, name='crear_reserva'),
    
    path('login/', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('reservas/listar/', views.listar_reservas, name='listar_reservas'),
    path('historial-medico/<int:mascota_id>/', views.historial_medico, name='historial_medico'),
    path('api/reserva/<int:id>/detalles/', views.obtener_detalles_reserva, name='obtener_detalles_reserva'),
    
    path('servicios/', views.servicios, name='servicios'),
    path('servicios/eliminar/<int:id>/', views.eliminar_servicio, name='eliminar_servicio'),
    
    path('clientes/listar/', views.listar_clientes, name='listar_clientes'),
    path('api/cliente/<int:id>/detalles/', views.obtener_detalles_cliente, name='obtener_detalles_cliente'),
    
    path('historial-medico-completo/<int:mascota_id>/', views.historial_medico_completo, name='historial_medico_completo'),
]
