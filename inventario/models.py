from django.db import models
from django.core.validators import RegexValidator


# 1. Categoría
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'categoria'

    def __str__(self):
        return self.nombre

# 2. Producto
class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    class Meta:
        db_table = 'producto'

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"

# 3. Cliente
class Cliente(models.Model):
    cedula = models.CharField(
        max_length=10,
        unique=True,
        validators=[RegexValidator(r'^\d{6,10}$',
        'La cédula debe tener entre 6 y 10 dígitos.')]
    )
    nombre = models.CharField(max_length=120)
    telefono = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\d{7,10}$',
        'El teléfono debe tener entre 7 y 10 dígitos.')]
    )
    correo = models.EmailField()
    direccion = models.CharField(max_length=250)

    class Meta:
        db_table = 'cliente'

    def __str__(self):
        return f"{self.nombre} ({self.cedula})"

# 4. Venta
class Venta(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='ventas')
    total = models.DecimalField(max_digits=12, decimal_places=2)
    estado = models.CharField(max_length=50, default='Pendiente')

    class Meta:
        db_table = 'venta'

    def __str__(self):
        return f"Venta #{self.id} - {self.cliente.nombre}"