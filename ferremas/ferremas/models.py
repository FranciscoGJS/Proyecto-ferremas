# filepath: ferremas/ferremas/models.py
from django.db import models

class PagoTransferencia(models.Model):
    usuario = models.CharField(max_length=100)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, default='pendiente')
    detalles = models.TextField(blank=True, null=True)
    tipo_pago = models.CharField(max_length=20, default='transferencia')