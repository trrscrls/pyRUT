"""
PyRUT - Librería Python para validación de RUTs y RUNs chilenos.

Esta librería proporciona herramientas para validar, calcular y formatear
RUTs (Rol Único Tributario) y RUNs (Rol Único Nacional) chilenos utilizando 
el algoritmo oficial de módulo 11.

Nota: En Chile, RUT y RUN usan el mismo formato y algoritmo de validación.
- RUN: Número de cédula de identidad (personas)
- RUT: Rol tributario (empresas y personas para efectos fiscales)

Uso básico:
    >>> from pyrut import ValidadorRUT, ValidadorRUN
    >>> ValidadorRUT.validar("12.345.678-5")
    True
    >>> ValidadorRUN.validar("12.345.678-5")  # Mismo resultado
    True
    >>> ValidadorRUT.calcular_digito_verificador(12345678)
    '5'
    >>> ValidadorRUT.formatear("123456785")
    '12.345.678-5'

Características:
    - Validación completa de RUTs/RUNs con algoritmo módulo 11
    - Cálculo de dígito verificador
    - Formateo flexible (con/sin puntos)
    - Limpieza y normalización
    - Validación de listas
    - Manejo de 'K' como dígito verificador
    - Sin dependencias externas

Autor: PyRUT Team
Licencia: MIT
"""

__version__ = "1.0.0"
__author__ = "PyRUT Team"
__license__ = "MIT"

from .core import ValidadorRUT, RUTInvalidoError

# Alias para RUN (mismo algoritmo que RUT)
ValidadorRUN = ValidadorRUT

__all__ = [
    "ValidadorRUT",
    "ValidadorRUN",
    "RUTInvalidoError",
    "__version__",
]
