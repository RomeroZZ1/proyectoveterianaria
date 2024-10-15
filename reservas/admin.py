from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import Usuario, Mascota, Servicio, Reserva, HistorialMedico

class UsuarioAdmin(DefaultUserAdmin):
    model = Usuario
    list_display = ('username', 'nombre', 'apellidos', 'rol', 'identificacion', 'celular', 'correo', 'fecha_nacimiento')
    search_fields = ('username', 'nombre', 'apellidos', 'identificacion', 'correo')
    list_filter = ('rol',)
    ordering = ('-fecha_nacimiento',)
    fieldsets = (
        (None, {
            'fields': ('username', 'nombre', 'apellidos', 'rol', 'identificacion', 'celular', 'correo', 'fecha_nacimiento')
        }),
        ('Permisos', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions', 'groups'),
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'nombre', 'apellidos', 'rol', 'identificacion', 'celular', 'correo', 'fecha_nacimiento'),
        }),
    )
    filter_horizontal = ('user_permissions', 'groups')

admin.site.register(Usuario, UsuarioAdmin)

# Registro de los otros modelos

@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'raza', 'sexo', 'edad', 'cliente', 'carnet_vacunacion')
    search_fields = ('nombre', 'tipo', 'raza', 'cliente__nombre')
    list_filter = ('tipo', 'raza', 'sexo', 'cliente')
    ordering = ('-fecha_nacimiento',)
    fieldsets = (
        (None, {
            'fields': ('nombre', 'tipo', 'raza', 'sexo', 'edad', 'fecha_nacimiento', 'carnet_vacunacion', 'cliente')
        }),
    )

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'precio', 'tiempo')
    search_fields = ('titulo',)
    ordering = ('titulo',)
    fieldsets = (
        (None, {
            'fields': ('titulo', 'descripcion', 'precio', 'tiempo')
        }),
    )

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'mascota', 'fecha', 'hora')
    search_fields = ('cliente__nombre', 'mascota__nombre', 'fecha')
    list_filter = ('fecha', 'hora', 'cliente', 'mascota')
    ordering = ('-fecha', '-hora')
    fieldsets = (
        (None, {
            'fields': ('cliente', 'mascota', 'servicios', 'fecha', 'hora', 'notas_adicionales')
        }),
    )

@admin.register(HistorialMedico)
class HistorialMedicoAdmin(admin.ModelAdmin):
    list_display = ('mascota', 'servicio', 'medico', 'titulo', 'fecha')
    search_fields = ('mascota__nombre', 'servicio__titulo', 'medico__nombre', 'titulo')
    list_filter = ('mascota', 'servicio', 'medico')
    ordering = ('-fecha',)
    fieldsets = (
        (None, {
            'fields': ('mascota', 'servicio', 'medico', 'titulo', 'descripcion', 'procedimiento', 'analisis', 'resultado', 'estado_animal', 'fecha')
        }),
    )
