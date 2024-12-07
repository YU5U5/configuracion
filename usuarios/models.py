from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Manager personalizado
class UsuarioManage(BaseUserManager):
    def create_user(self, correo_electronico, nombre, password=None, **extra_fields):
        if not correo_electronico:
            raise ValueError('El correo electrónico es obligatorio')
        correo_electronico = self.normalize_email(correo_electronico)
        usuario = self.model(correo_electronico=correo_electronico, nombre=nombre, **extra_fields)
        usuario.set_password(password)  # Usamos el método para hashear la contraseña
        usuario.save(using=self._db)
        return usuario
    
    def create_superuser(self, correo_electronico, nombre, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(correo_electronico, nombre, password, **extra_fields)

class Usuario(AbstractBaseUser):
    ESTADO = [
        ('activo', 'Activo'),
        ('pendiente_verificacion', 'Pendiente de Verificación'),
    ]

    nombre = models.CharField(max_length=100)  # 'NOT NULL' por defecto
    correo_electronico = models.EmailField(unique=True)  # 'NOT NULL' por defecto
    estado = models.CharField(max_length=30, choices=ESTADO, default='activo')  # 'NOT NULL' por defecto
    fecha_registro = models.DateTimeField(auto_now_add=True)  # 'NOT NULL' por defecto
    last_login = models.DateTimeField(null=True, blank=True)  # Agregamos el campo last_login

    # Usamos el manager personalizado
    objects = UsuarioManage()

    USERNAME_FIELD = 'correo_electronico'
    REQUIRED_FIELDS = ['nombre']  # 'nombre' es obligatorio en el formulario de creación

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'usuario'  # Aseguramos que se usa la tabla 'usuario'
        managed = False # Cambiamos a True para que Django gestione la tabla
