"""
Sistema Integral de Gestión de Clientes, Servicios y Reservas
Empresa: Software FJ
Curso: Programación 213023 - Fase 4 (Componente Práctico)
Estudiante: Cristian Antonio Berrio Herrera
Grupo: 132

Implementa:
- Abstracción, Herencia, Polimorfismo y Encapsulación
- Manejo avanzado de excepciones (personalizadas, try/except/else/finally, chaining)
- Sin bases de datos (listas + archivo de logs)
- Simulación de al menos 10 operaciones (válidas e inválidas)
"""

from abc import ABC, abstractmethod
from datetime import datetime
import os

# ==================== EXCEPCIONES PERSONALIZADAS ====================
class ErrorValidacion(Exception):
    """Excepción base para errores de validación."""
    pass

class ClienteInvalidoError(ErrorValidacion):
    pass

class ServicioNoDisponibleError(ErrorValidacion):
    pass

class ReservaInvalidaError(ErrorValidacion):
    pass

class DatosIncompletosError(ErrorValidacion):
    pass


# ==================== CLASE ABSTRACTA GENERAL ====================
class Entidad(ABC):
    """Clase abstracta que representa entidades generales del sistema."""

    @abstractmethod
    def validar(self):
        """Valida los datos de la entidad."""
        pass

    @abstractmethod
    def obtener_descripcion(self):
        """Retorna una descripción textual de la entidad."""
        pass


# ==================== CLASE CLIENTE (ENCAPSULACIÓN) ====================
class Cliente(Entidad):
    def __init__(self, nombre, identificacion, telefono, email):
        self._nombre = None
        self._identificacion = None
        self._telefono = None
        self._email = None
        self.nombre = nombre
        self.identificacion = identificacion
        self.telefono = telefono
        self.email = email
        self.validar()

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or len(valor.strip()) < 3:
            raise ClienteInvalidoError("El nombre debe tener al menos 3 caracteres.")
        self._nombre = valor.strip()

    @property
    def identificacion(self):
        return self._identificacion

    @identificacion.setter
    def identificacion(self, valor):
        if not valor or not str(valor).isdigit() or len(str(valor)) < 6:
            raise ClienteInvalidoError("La identificación debe ser numérica y tener al menos 6 dígitos.")
        self._identificacion = str(valor)

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        if valor and (not str(valor).isdigit() or len(str(valor)) < 7):
            raise ClienteInvalidoError("El teléfono debe contener solo números y tener al menos 7 dígitos.")
        self._telefono = str(valor) if valor else ""

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        if valor and ("@" not in valor or "." not in valor):
            raise ClienteInvalidoError("El email no tiene un formato válido.")
        self._email = valor.strip() if valor else ""

    def validar(self):
        if not self.nombre or not self.identificacion:
            raise DatosIncompletosError("Nombre e identificación son obligatorios.")

    def obtener_descripcion(self):
        return f"Cliente: {self.nombre} | ID: {self.identificacion}"


# ==================== CLASE ABSTRACTA SERVICIO ====================
class Servicio(Entidad, ABC):
    def __init__(self, nombre, precio_base, disponible=True):
        self.nombre = nombre
        self.precio_base = float(precio_base)
        self.disponible = disponible

    @abstractmethod
    def calcular_costo(self, duracion=1, impuesto=0.0, descuento=0.0):
        """Método sobrecargado simulado con parámetros opcionales."""
        pass

    @abstractmethod
    def describir_servicio(self):
        pass

    def validar(self):
        if self.precio_base <= 0:
            raise ServicioNoDisponibleError(f"El precio del servicio '{self.nombre}' debe ser mayor a cero.")
        if not self.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self.nombre}' no está disponible.")

    def obtener_descripcion(self):
        return self.describir_servicio()


# ==================== SERVICIOS ESPECIALIZADOS ====================
class ReservaSala(Servicio):
    def calcular_costo(self, duracion=1, impuesto=0.19, descuento=0.0):
        self.validar()
        if duracion <= 0:
            raise ReservaInvalidaError("La duración debe ser mayor a cero.")
        subtotal = self.precio_base * duracion
        con_descuento = subtotal * (1 - descuento / 100)
        return round(con_descuento * (1 + impuesto), 2)

    def describir_servicio(self):
        return f"Reserva de Sala | Precio/hora: ${self.precio_base:.2f} | Disponible: {self.disponible}"


class AlquilerEquipo(Servicio):
    def calcular_costo(self, duracion=1, impuesto=0.19, descuento=0.0):
        self.validar()
        if duracion <= 0:
            raise ReservaInvalidaError("La duración debe ser mayor a cero.")
        subtotal = self.precio_base * duracion
        con_descuento = subtotal * (1 - descuento / 100)
        return round(con_descuento * (1 + impuesto), 2)

    def describir_servicio(self):
        return f"Alquiler de Equipo | Precio/día: ${self.precio_base:.2f} | Disponible: {self.disponible}"


class AsesoriaEspecializada(Servicio):
    def calcular_costo(self, duracion=1, impuesto=0.19, descuento=0.0):
        self.validar()
        if duracion <= 0:
            raise ReservaInvalidaError("La duración debe ser mayor a cero.")
        subtotal = self.precio_base * duracion
        con_descuento = subtotal * (1 - descuento / 100)
        return round(con_descuento * (1 + impuesto), 2)

    def describir_servicio(self):
        return f"Asesoría Especializada | Precio/hora: ${self.precio_base:.2f} | Disponible: {self.disponible}"


# ==================== CLASE RESERVA ====================
class Reserva:
    def __init__(self, cliente, servicio, duracion, estado="Pendiente"):
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = estado
        self.costo = 0.0
        self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M")

    def confirmar(self, impuesto=0.19, descuento=0.0):
        try:
            self.costo = self.servicio.calcular_costo(self.duracion, impuesto, descuento)
            self.estado = "Confirmada"
            return True
        except Exception as e:
            raise ReservaInvalidaError(f"No se pudo confirmar la reserva: {e}") from e

    def cancelar(self):
        if self.estado == "Cancelada":
            raise ReservaInvalidaError("La reserva ya está cancelada.")
        self.estado = "Cancelada"
        return True

    def procesar(self):
        if self.estado != "Confirmada":
            raise ReservaInvalidaError("Solo se pueden procesar reservas confirmadas.")
        self.estado = "Procesada"
        return True
