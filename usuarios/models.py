from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Manager personalizado para el modelo de usuario
class UsuarioManage(BaseUserManager):
    def create_user(self, correo_electronico, nombre, password=None, **extra_fields):
        if not correo_electronico:
            raise ValueError('El correo electrónico es obligatorio')
        correo_electronico = self.normalize_email(correo_electronico)
        usuario = self.model(correo_electronico=correo_electronico, nombre=nombre, **extra_fields)
        usuario.set_password(password)  # Hashea la contraseña
        usuario.save(using=self._db)
        return usuario
    
    def create_superuser(self, correo_electronico, nombre, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(correo_electronico, nombre, password, **extra_fields)


class Usuario(AbstractBaseUser):
    ESTADO = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
    ]

    nombre = models.CharField(max_length=100)
    correo_electronico = models.EmailField(unique=True)
    estado = models.CharField(max_length=10, choices=ESTADO, default='Activo')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UsuarioManage()

    USERNAME_FIELD = 'correo_electronico'
    REQUIRED_FIELDS = ['nombre']

    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = 'usuario'
