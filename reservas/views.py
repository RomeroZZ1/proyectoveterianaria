from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import timedelta
import re
from django.db.models.functions import TruncMonth
from django.urls import reverse
from django.db.models import Q
from django.http import JsonResponse
import random
from django.db.models import Sum
from django.contrib.auth.hashers import make_password
from django.db import transaction
from reservas.models import Usuario, Mascota, Reserva, Servicio, HistorialMedico
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta
from django.utils import timezone
from django.utils.translation import gettext as _
from reservas import models

def inicio(request):
    return render(request, 'inicio.html')

def reservar_servicio(request):
    if request.method == 'POST':
        email_cliente = request.POST.get('email_cliente')
        telefono_cliente = request.POST.get('telefono_cliente')
        nombre_cliente = request.POST.get('nombre_cliente')
        apellidos_cliente = request.POST.get('apellidos_cliente')
        identificacion_cliente = request.POST.get('identificacion_cliente')
        fecha_nacimiento_cliente = request.POST.get('fecha_nacimiento_cliente')
        nombre_mascota = request.POST.get('nombre_mascota')
        tipo_mascota = request.POST.get('tipo_mascota')
        raza_mascota = request.POST.get('raza_mascota')
        sexo_mascota = request.POST.get('sexo_mascota')
        edad_mascota = request.POST.get('edad_mascota')
        fecha_nacimiento_mascota = request.POST.get('fecha_nacimiento_mascota')
        carnet_vacunacion = request.POST.get('carnet_vacunacion') == 'true'
        fecha_reserva = request.POST.get('fecha_reserva')
        hora_reserva = request.POST.get('hora_reserva')
        servicios = request.POST.getlist('servicios')
        notas_adicionales = request.POST.get('notas_adicionales')

        cliente, creado = Usuario.objects.get_or_create(
            correo=email_cliente,
            defaults={
                'nombre': nombre_cliente,
                'apellidos': apellidos_cliente,
                'identificacion': identificacion_cliente,
                'celular': telefono_cliente,
                'fecha_nacimiento': fecha_nacimiento_cliente,
                'rol': 'cliente'
            }
        )
        if not creado:
            cliente.nombre = nombre_cliente
            cliente.apellidos = apellidos_cliente
            cliente.celular = telefono_cliente
            cliente.fecha_nacimiento = fecha_nacimiento_cliente
            cliente.save()

        mascota, mascota_creada = Mascota.objects.get_or_create(
            cliente=cliente,
            nombre=nombre_mascota,
            defaults={
                'tipo': tipo_mascota,
                'raza': raza_mascota,
                'sexo': sexo_mascota,
                'edad': edad_mascota,
                'fecha_nacimiento': fecha_nacimiento_mascota,
                'carnet_vacunacion': carnet_vacunacion
            }
        )
        if not mascota_creada:
            mascota.tipo = tipo_mascota
            mascota.raza = raza_mascota
            mascota.sexo = sexo_mascota
            mascota.edad = edad_mascota
            mascota.fecha_nacimiento = fecha_nacimiento_mascota
            mascota.carnet_vacunacion = carnet_vacunacion
            mascota.save()

        # Verificar disponibilidad de la hora
        if Reserva.objects.filter(fecha=fecha_reserva, hora=hora_reserva).exists():
            messages.error(request, 'La hora seleccionada ya está reservada.')
            return redirect('dashboard')

        reserva = Reserva.objects.create(
            cliente=cliente,
            mascota=mascota,
            fecha=fecha_reserva,
            hora=hora_reserva,
            notas_adicionales=notas_adicionales
        )
        reserva.servicios.set(servicios)

        messages.success(request, 'Reserva realizada con éxito.')
        return redirect('dashboard')

    servicios_list = Servicio.objects.all()
    tipos_mascota = Mascota.TIPOS_MASCOTA
    sexos = Mascota.SEXOS
    context = {
        'servicios': servicios_list,
        'tipos_mascota': tipos_mascota,
        'sexos': sexos
    }
    return render(request, 'reservar_servicio.html', context)

def obtener_razas(request):
    tipo_mascota = request.GET.get('tipo')
    if tipo_mascota in Mascota.RAZAS:
        razas = Mascota.RAZAS[tipo_mascota]
        return JsonResponse(razas, safe=False)
    return JsonResponse([], safe=False)

def obtener_servicios(request):
    servicios = Servicio.objects.all().values('id', 'titulo')
    return JsonResponse(list(servicios), safe=False)

def generate_username(name):
    username = ''.join(e for e in name if e.isalnum()).lower()
    while Usuario.objects.filter(username=username).exists():
        username = username + str(random.randint(0, 9999))
    return username

from django.db import transaction
from django.http import JsonResponse
from .models import Usuario, Mascota, Reserva, Servicio
import random
import string
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def crear_reserva(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                email = request.POST.get('email')
                nombre = request.POST.get('firstName')
                apellidos = request.POST.get('lastName')
                identificacion = request.POST.get('identification')
                celular = request.POST.get('cellphone')
                fecha_nacimiento = request.POST.get('birthdate')

                # Verifica si el usuario ya existe
                usuario = Usuario.objects.filter(identificacion=identificacion).first()

                if not usuario:
                    # Genera un nombre de usuario único
                    username_base = f"{nombre.lower()}{random.randint(1000, 9999)}"
                    while Usuario.objects.filter(username=username_base).exists():
                        username_base = f"{nombre.lower()}{random.randint(1000, 9999)}"

                    # Crea el nuevo usuario
                    usuario = Usuario.objects.create(
                        username=username_base,
                        nombre=nombre,
                        apellidos=apellidos,
                        identificacion=identificacion,
                        celular=celular,
                        correo=email,
                        fecha_nacimiento=fecha_nacimiento,
                        rol='cliente'
                    )
                    usuario.set_password(identificacion)  # La contraseña es la identificación
                    usuario.save()

                    mensaje = f"Se creó el usuario con el nombre de usuario: {usuario.username} y contraseña: {identificacion}"
                else:
                    mensaje = f"Se encontró un usuario existente con el nombre de usuario: {usuario.username}"

                # Crea la mascota
                mascota = Mascota.objects.create(
                    cliente=usuario,
                    nombre=request.POST.get('petName'),
                    edad=request.POST.get('petAge'),
                    fecha_nacimiento=request.POST.get('petBirthdate'),
                    carnet_vacunacion=request.POST.get('vaccinationCard') == 'on',
                    tipo=request.POST.get('petType'),
                    raza=request.POST.get('petBreed'),
                    sexo=request.POST.get('petSex'),
                )

                # Crea la reserva
                reserva = Reserva.objects.create(
                    cliente=usuario,
                    mascota=mascota,
                    fecha=request.POST.get('reservationDate'),
                    hora=request.POST.get('reservationTime'),
                    notas_adicionales=request.POST.get('notes')
                )

                # Agrega los servicios a la reserva
                servicios = request.POST.getlist('service')
                for servicio_id in servicios:
                    servicio = Servicio.objects.get(id=servicio_id)
                    reserva.servicios.add(servicio)

                reserva.save()

                return JsonResponse({'success': True, 'message': mensaje})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    # Si no es POST, retornamos un error (esto es opcional dependiendo de tu lógica)
    return JsonResponse({'success': False, 'message': 'Método no permitido.'}, status=405)



def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    return render(request, 'login.html')

@login_required
def dashboard(request):
    # Totales generales
    total_clientes = Usuario.objects.filter(rol='cliente').count()
    total_medicos = Usuario.objects.filter(rol='medico').count()
    total_mascotas = Mascota.objects.count()
    total_reservas = Reserva.objects.count()

    # Ingresos totales
    total_ingresos = Reserva.objects.aggregate(total=Sum('servicios__precio'))['total'] or 0

    # Ingresos por los últimos 6 meses
    six_months_ago = timezone.now() - timedelta(days=180)
    ingresos_por_mes = Reserva.objects.filter(fecha__gte=six_months_ago).annotate(
        mes=TruncMonth('fecha')
    ).values('mes').annotate(
        total=Sum('servicios__precio')
    ).order_by('mes')

    # Reservas por día de la última semana
    one_week_ago = timezone.now() - timedelta(days=7)
    reservas_por_dia = Reserva.objects.filter(fecha__gte=one_week_ago).values('fecha').annotate(
        total=Count('id')
    ).order_by('fecha')

    # Actividades recientes (las últimas 5 reservas)
    actividades_recientes = Reserva.objects.select_related('cliente', 'mascota').order_by('-fecha', '-hora')[:5]

    context = {
        'total_clientes': total_clientes,
        'total_medicos': total_medicos,
        'total_mascotas': total_mascotas,
        'total_reservas': total_reservas,
        'total_ingresos': total_ingresos,
        'ingresos_por_mes': ingresos_por_mes,
        'reservas_por_dia': reservas_por_dia,
        'actividades_recientes': actividades_recientes,
    }
    return render(request, 'dashboard.html', context)


@login_required
def servicios(request):
    username = request.user.username
    servicios_list = Servicio.objects.all()

    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        tiempo_str = request.POST.get('tiempo')
        
        if titulo and descripcion and precio and tiempo_str:
            try:
                # Convertir precio a float
                precio = float(precio)
                
                # Convertir tiempo a timedelta
                tiempo_match = re.match(r'(\d+):(\d+):(\d+)', tiempo_str)
                if tiempo_match:
                    horas, minutos, segundos = map(int, tiempo_match.groups())
                    tiempo = timedelta(hours=horas, minutes=minutos, seconds=segundos)
                else:
                    # Manejar el caso en que el formato de tiempo es incorrecto
                    return redirect('servicios')

                Servicio.objects.create(
                    titulo=titulo,
                    descripcion=descripcion,
                    precio=precio,
                    tiempo=tiempo
                )
            except ValueError:
                # Manejar error en caso de formato incorrecto de precio
                return redirect('servicios')

        return redirect('servicios')

    context = {
        'username': username,
        'servicios': servicios_list
    }
    return render(request, 'servicios.html', context)

@login_required
def eliminar_servicio(request, id):
    if request.method == 'POST':
        Servicio.objects.filter(id=id).delete()
    return redirect('servicios')

def listar_reservas(request):
    # Obtener todas las reservas ordenadas de la más antigua a la más reciente
    reservas = Reserva.objects.all().order_by('fecha', 'hora')

    # Filtrar por búsqueda (opcional)
    search_query = request.GET.get('search', '')
    if search_query:
        reservas = reservas.filter(
            Q(cliente__nombre__icontains=search_query) |
            Q(cliente__apellidos__icontains=search_query) |
            Q(mascota__nombre__icontains=search_query) |
            Q(servicios__titulo__icontains=search_query)
        ).distinct()
        
    context = {
        'reservas': reservas,
        'search_query': search_query
    }
    return render(request, 'lista_reservas.html', context)

def obtener_detalles_reserva(request, id):
    reserva = Reserva.objects.get(id=id)
    detalles = {
        'cliente': {
            'nombre': reserva.cliente.nombre,
            'apellidos': reserva.cliente.apellidos,
            'correo': reserva.cliente.correo,
            'celular': reserva.cliente.celular,
            'identificacion': reserva.cliente.identificacion,
            'fecha_nacimiento': reserva.cliente.fecha_nacimiento
        },
        'mascota': {
            'nombre': reserva.mascota.nombre,
            'edad': reserva.mascota.edad,
            'fecha_nacimiento': reserva.mascota.fecha_nacimiento,
            'tipo': reserva.mascota.tipo,
            'raza': reserva.mascota.raza,
            'sexo': reserva.mascota.sexo,
        },
        'fecha': reserva.fecha,
        'hora': reserva.hora,
        'servicios': [servicio.titulo for servicio in reserva.servicios.all()],
        'notas_adicionales': reserva.notas_adicionales,
    }
    return JsonResponse(detalles)

def listar_clientes(request):
    # Usa el related_name correcto para prefetch_related
    clientes = Usuario.objects.filter(rol='cliente').prefetch_related('mascotas')

    context = {
        'clientes': clientes,
    }
    return render(request, 'lista_clientes.html', context)

def obtener_detalles_cliente(request, id):
    cliente = Usuario.objects.get(id=id, rol='cliente')
    mascotas = Mascota.objects.filter(cliente=cliente)

    detalles = {
        'nombre': cliente.nombre,
        'apellidos': cliente.apellidos,
        'correo': cliente.correo,
        'celular': cliente.celular,
        'identificacion': cliente.identificacion,
        'fecha_nacimiento': cliente.fecha_nacimiento,
        'mascotas': [{
            'id': mascota.id,  # Aseguramos que el ID de la mascota esté presente aquí
            'nombre': mascota.nombre,
            'edad': mascota.edad,
            'fecha_nacimiento': str(mascota.fecha_nacimiento),
            'tipo': mascota.tipo,
            'raza': mascota.raza,
            'sexo': mascota.sexo,
        } for mascota in mascotas],
    }
    
    return JsonResponse(detalles)




from django.contrib.auth.decorators import login_required

@login_required
def historial_medico_completo(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)
    historiales = HistorialMedico.objects.filter(mascota=mascota).order_by('-fecha')

    context = {
        'mascota': mascota,
        'historiales': historiales
    }

    return render(request, 'historial_medico_completo.html', context)


def obtener_detalles_cliente(request, id):
    cliente = Usuario.objects.get(id=id, rol='cliente')
    mascotas = Mascota.objects.filter(cliente=cliente)
    
    detalles = {
        'nombre': cliente.nombre,
        'apellidos': cliente.apellidos,
        'correo': cliente.correo,
        'celular': cliente.celular,
        'identificacion': cliente.identificacion,
        'fecha_nacimiento': cliente.fecha_nacimiento,
        'mascotas': [{
            'nombre': mascota.nombre,
            'edad': mascota.edad,
            'fecha_nacimiento': mascota.fecha_nacimiento,
            'tipo': mascota.tipo,
            'raza': mascota.raza,
            'sexo': mascota.sexo,
        } for mascota in mascotas],
    }
    
    return JsonResponse(detalles)

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from django.utils import timezone

from django.contrib import messages
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

def historial_medico(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)
    historiales = HistorialMedico.objects.filter(mascota=mascota).order_by('-fecha')
    servicios = Servicio.objects.all()
    medicos = Usuario.objects.filter(rol='medico')

    # Obtener la fecha actual
    fecha_actual = timezone.localtime(timezone.now())
    
    if request.method == 'POST':
        try:
            # Obtener el servicio seleccionado desde el formulario
            servicio_id = request.POST.get('servicio')
            servicio = get_object_or_404(Servicio, id=servicio_id)

            # Recolectamos los demás datos del formulario
            antecedentes = request.POST.get('antecedentes')
            acompanante = request.POST.get('acompanante')
            diagnostico = request.POST.get('diagnostico')
            temperatura = request.POST.get('temperatura')
            peso = request.POST.get('peso')
            frecuencia_cardiaca = request.POST.get('frecuencia_cardiaca')
            frecuencia_respiratoria = request.POST.get('frecuencia_respiratoria')
            esterilizado = request.POST.get('esterilizado') == 'si'
            color = request.POST.get('color')
            dieta = request.POST.get('dieta')
            partos = request.POST.get('partos') == 'si'
            procedimiento = request.POST.get('procedimiento')
            analisis = request.POST.get('analisis')
            medico = request.user if request.user.rol == 'medico' else get_object_or_404(Usuario, id=request.POST.get('medico'))

            # Obtener la fecha del formulario o asignar la fecha actual si no se proporciona
            fecha = request.POST.get('fecha', timezone.localdate())

            # Construimos el título automáticamente
            titulo = f"{mascota.nombre} - {servicio.titulo} - {medico.nombre}"

            # Guardamos en el modelo
            HistorialMedico.objects.create(
                mascota=mascota,
                medico=medico,
                servicio=servicio,
                titulo=titulo,
                procedimiento=procedimiento,
                analisis=analisis,
                fecha=fecha,
                antecedentes=antecedentes,
                acompanante=acompanante,
                diagnostico=diagnostico,
                temperatura=temperatura,
                peso=peso,
                frecuencia_cardiaca=frecuencia_cardiaca,
                frecuencia_respiratoria=frecuencia_respiratoria,
                esterilizado=esterilizado,
                color=color,
                dieta=dieta,
                partos=partos,
            )

            # Mensaje de éxito
            messages.success(request, 'Historial médico guardado correctamente.')
            return redirect(reverse('historial_medico', args=[mascota_id]))

        except Exception as e:
            # Mensaje de error
            messages.error(request, f'Error al guardar el historial médico: {str(e)}')

    context = {
        'mascota': mascota,
        'historiales': historiales,
        'servicios': servicios,
        'medicos': medicos,
        'fecha_actual': fecha_actual,
    }
    
    return render(request, 'historial_medico.html', context)

