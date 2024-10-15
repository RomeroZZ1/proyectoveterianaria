from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings  # Para referenciar AUTH_USER_MODEL

class Usuario(AbstractUser):
    ROLES = [
        ('administrador', 'Administrador'),
        ('cliente', 'Cliente'),
        ('medico', 'Medico'),
    ]
    rol = models.CharField(max_length=13, choices=ROLES)
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    identificacion = models.CharField(max_length=20, unique=True)
    celular = models.CharField(max_length=15)
    correo = models.EmailField(unique=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)

    # Especifica un `related_name` único para evitar conflictos
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuario_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuario_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return f"{self.nombre} {self.apellidos} - {self.rol}"

# Modelo de Mascota
class Mascota(models.Model):
    TIPOS_MASCOTA = [
        ('perro', 'Perro'),
        ('gato', 'Gato'),
        ('caballo', 'Caballo'),
        ('hamster', 'Hamster'),
        ('pajaro', 'Pájaro'),
        ('conejo', 'Conejo'),
        ('pez', 'Pez'),
        ('reptil', 'Reptil'),
        ('roedor', 'Roedor'),
        ('huron', 'Hurón'),
        ('otro', 'Otro'),
    ]
    
    SEXOS = [
        ('macho', 'Macho'),
        ('hembra', 'Hembra'),
    ]
    
    # Diccionario de razas según el tipo de mascota
    RAZAS = {
        'perro': [
            ('labrador', 'Labrador Retriever'),
            ('pastor_aleman', 'Pastor Alemán'),
            ('bulldog', 'Bulldog'),
            ('poodle', 'Poodle'),
            ('beagle', 'Beagle'),
            ('chihuahua', 'Chihuahua'),
            ('golden_retriever', 'Golden Retriever'),
            ('dachshund', 'Dachshund'),
            ('rottweiler', 'Rottweiler'),
            ('doberman', 'Doberman'),
            ('yorkshire_terrier', 'Yorkshire Terrier'),
            ('boxer', 'Boxer'),
            ('husky_siberiano', 'Husky Siberiano'),
            ('dalmata', 'Dálmata'),
            ('shih_tzu', 'Shih Tzu'),
            ('pomerania', 'Pomerania'),
            ('cocker_spaniel', 'Cocker Spaniel'),
            ('akita', 'Akita'),
            ('otro', 'Otro'),
        ],
        'gato': [
            ('siames', 'Siamés'),
            ('persa', 'Persa'),
            ('maine_coon', 'Maine Coon'),
            ('ragdoll', 'Ragdoll'),
            ('sphynx', 'Sphynx'),
            ('bengali', 'Bengalí'),
            ('britanico_de_pelo_corto', 'Británico de Pelo Corto'),
            ('exotico_de_pelo_corto', 'Exótico de Pelo Corto'),
            ('himalayo', 'Himalayo'),
            ('birmano', 'Birmano'),
            ('angora', 'Angora'),
            ('manx', 'Manx'),
            ('otro', 'Otro'),
        ],
        'caballo': [
            ('pura_sangre', 'Pura Sangre'),
            ('andaluz', 'Andaluz'),
            ('percheron', 'Percherón'),
            ('cuarto_de_milla', 'Cuarto de Milla'),
            ('frison', 'Frisón'),
            ('appaloosa', 'Appaloosa'),
            ('pinto', 'Pinto'),
            ('arabe', 'Árabe'),
            ('mustang', 'Mustang'),
            ('belga', 'Belga'),
            ('morgan', 'Morgan'),
            ('tennessee_walker', 'Tennessee Walker'),
            ('haflinger', 'Haflinger'),
            ('otro', 'Otro'),
        ],
        'hamster': [
            ('sirio', 'Hamster Sirio'),
            ('ruso', 'Hamster Ruso'),
            ('roborovski', 'Hamster Roborovski'),
            ('chino', 'Hamster Chino'),
            ('campbell', 'Hamster Campbell'),
            ('europeo', 'Hamster Europeo'),
            ('albino', 'Hamster Albino'),
            ('otro', 'Otro'),
        ],
        'pajaro': [
            ('canario', 'Canario'),
            ('periquito', 'Periquito'),
            ('agaporni', 'Agaporni'),
            ('loro', 'Loro'),
            ('cacatua', 'Cacatúa'),
            ('guacamayo', 'Guacamayo'),
            ('diamante_mandarin', 'Diamante Mandarín'),
            ('pinzon', 'Pinzón'),
            ('ninfa', 'Ninfa'),
            ('cotorras', 'Cotorras'),
            ('paloma', 'Paloma'),
            ('gorrion', 'Gorrión'),
            ('colibri', 'Colibrí'),
            ('otro', 'Otro'),
        ],
        'conejo': [
            ('conejo_holandes', 'Conejo Holandés'),
            ('belier', 'Belier'),
            ('rex', 'Rex'),
            ('angora', 'Angora'),
            ('lop', 'Lop'),
            ('himalayo', 'Himalayo'),
            ('mini_rex', 'Mini Rex'),
            ('flandes', 'Gigante de Flandes'),
            ('californiano', 'Californiano'),
            ('otro', 'Otro'),
        ],
        'pez': [
            ('betta', 'Betta'),
            ('goldfish', 'Goldfish'),
            ('pez_angel', 'Pez Ángel'),
            ('pez_guppy', 'Guppy'),
            ('neon', 'Neón'),
            ('disco', 'Disco'),
            ('ciclido', 'Cíclido'),
            ('carpa', 'Carpa'),
            ('koi', 'Koi'),
            ('pleco', 'Pleco'),
            ('tiburon_bala', 'Tiburón Bala'),
            ('pez_payaso', 'Pez Payaso'),
            ('pez_globo', 'Pez Globo'),
            ('pez_oscuro', 'Pez Óscar'),
            ('pez_tetra', 'Pez Tetra'),
            ('pez_arcoiris', 'Pez Arcoíris'),
            ('pez_espada', 'Pez Espada'),
            ('otro', 'Otro'),
        ],
        'reptil': [
            ('iguana', 'Iguana'),
            ('gecko', 'Gecko'),
            ('serpiente', 'Serpiente'),
            ('camaleon', 'Camaleón'),
            ('tortuga', 'Tortuga'),
            ('dragon_barbudo', 'Dragón Barbudo'),
            ('anolis', 'Anolis'),
            ('boa', 'Boa'),
            ('piton', 'Pitón'),
            ('lagarto', 'Lagarto'),
            ('caiman', 'Caimán'),
            ('otro', 'Otro'),
        ],
        'roedor': [
            ('cobaya', 'Cobaya'),
            ('raton', 'Ratón'),
            ('rata', 'Rata'),
            ('chinchilla', 'Chinchilla'),
            ('jerbo', 'Jerbo'),
            ('dumbo', 'Dumbo'),
            ('capibara', 'Capibara'),
            ('paca', 'Paca'),
            ('aguti', 'Agutí'),
            ('coendu', 'Coendú'),
            ('otro', 'Otro'),
        ],
        'huron': [
            ('huron', 'Hurón Doméstico'),
            ('albino', 'Hurón Albino'),
            ('angora', 'Hurón Angora'),
            ('otro', 'Otro'),
        ],
        'otro': [
            ('otro', 'Otro'),
        ],
    }

    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mascotas'  # Verifica si el related_name está configurado aquí
    )
    nombre = models.CharField(max_length=50)
    edad = models.IntegerField()
    fecha_nacimiento = models.DateField()
    carnet_vacunacion = models.BooleanField(default=False)
    tipo = models.CharField(max_length=10, choices=TIPOS_MASCOTA)
    raza = models.CharField(max_length=50)
    sexo = models.CharField(max_length=6, choices=SEXOS)

    def __str__(self):
        return f"{self.nombre} - {self.tipo} ({self.raza}) ({self.sexo})"
    
    def save(self, *args, **kwargs):
        # Validación de raza según el tipo de mascota
        if self.tipo in self.RAZAS:
            raza_choices = dict(self.RAZAS[self.tipo])
            if self.raza not in raza_choices:
                raise ValueError(f"La raza '{self.raza}' no es válida para el tipo de mascota '{self.tipo}'.")
        super(Mascota, self).save(*args, **kwargs)

# Modelo de Servicio
class Servicio(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    tiempo = models.DurationField()

    def __str__(self):
        return f"{self.titulo} - ${self.precio}"

# Modelo de Reserva
class Reserva(models.Model):
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='reservas', limit_choices_to={'rol': 'cliente'})
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='reservas')
    servicios = models.ManyToManyField(Servicio, related_name='reservas')
    fecha = models.DateField()
    hora = models.TimeField()
    notas_adicionales = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Reserva de {self.cliente.nombre} para {self.mascota.nombre} el {self.fecha} a las {self.hora}"

# Modelo de Historial Médico
class HistorialMedico(models.Model):
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='historiales')
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='historiales')
    medico = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='historiales', limit_choices_to={'rol': 'medico'})
    titulo = models.CharField(max_length=100)
    procedimiento = models.TextField()
    analisis = models.TextField()
    fecha = models.DateField()
    
    # Nuevos campos añadidos
    antecedentes = models.TextField()  # Antecedentes o enfermedad actual
    acompanante = models.CharField(max_length=100)  # Nombre del acompañante
    diagnostico = models.TextField()
    temperatura = models.DecimalField(max_digits=4, decimal_places=1)  # Temperatura en °C
    peso = models.DecimalField(max_digits=5, decimal_places=2)  # Peso en KG
    frecuencia_cardiaca = models.IntegerField()  # Frecuencia cardiaca en pulsaciones por minuto
    frecuencia_respiratoria = models.IntegerField()  # Frecuencia respiratoria por minuto
    esterilizado = models.BooleanField()  # Esterilizado Sí o No
    color = models.CharField(max_length=30)  # Color de la mascota
    dieta = models.TextField()  # Descripción de la dieta
    partos = models.BooleanField(null=True, blank=True)  # Partos Sí o No (opcional)

    def __str__(self):
        return f"Historial de {self.mascota.nombre} para {self.servicio.titulo} por {self.medico.nombre}"
