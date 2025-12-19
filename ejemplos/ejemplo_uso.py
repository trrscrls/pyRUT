"""
Ejemplos de uso de PyRUT - Librería de validación de RUTs chilenos.

Este archivo contiene ejemplos prácticos de cómo utilizar la librería
PyRUT para diferentes casos de uso comunes.

Para ejecutar estos ejemplos:
    python examples/ejemplo_uso.py
"""

from pyrut import ValidadorRUT, RUTInvalidoError


def ejemplo_validacion_simple():
    """Ejemplo 1: Validación simple de RUTs."""
    print("=" * 60)
    print("EJEMPLO 1: Validación Simple de RUTs")
    print("=" * 60)
    
    ruts_a_validar = [
        "12.345.678-5",   # Válido con puntos
        "12345678-5",     # Válido sin puntos
        "123456785",      # Válido sin separadores
        "12.345.678-K",   # Con K (verificar si es válido)
        "12.345.678-0",   # Inválido (dígito incorrecto)
        "11.111.111-1",   # Válido
        "22.222.222-2",   # Válido
    ]
    
    for rut in ruts_a_validar:
        es_valido = ValidadorRUT.validar(rut)
        estado = "✓ Válido" if es_valido else "✗ Inválido"
        print(f"  {rut:20} -> {estado}")
    
    print()


def ejemplo_calculo_digito_verificador():
    """Ejemplo 2: Cálculo de dígito verificador."""
    print("=" * 60)
    print("EJEMPLO 2: Cálculo de Dígito Verificador")
    print("=" * 60)
    
    numeros = [
        12345678,
        11111111,
        22222222,
        33333333,
        9007890,
        18885542,
    ]
    
    for numero in numeros:
        digito = ValidadorRUT.calcular_digito_verificador(numero)
        rut_completo = ValidadorRUT.formatear(f"{numero}{digito}")
        print(f"  {numero:,} -> Dígito: {digito} -> RUT: {rut_completo}")
    
    print()


def ejemplo_formateo():
    """Ejemplo 3: Formateo y limpieza de RUTs."""
    print("=" * 60)
    print("EJEMPLO 3: Formateo y Limpieza de RUTs")
    print("=" * 60)
    
    ruts = [
        "123456785",
        "12345678-5",
        "12.345.678-5",
        "  12 345 678 5  ",  # Con espacios
    ]
    
    print("\n  Formateo CON puntos:")
    for rut in ruts:
        try:
            formateado = ValidadorRUT.formatear(rut, con_puntos=True)
            print(f"    '{rut}' -> '{formateado}'")
        except RUTInvalidoError as e:
            print(f"    '{rut}' -> Error: {e}")
    
    print("\n  Formateo SIN puntos:")
    for rut in ruts[:3]:
        formateado = ValidadorRUT.formatear(rut, con_puntos=False)
        print(f"    '{rut}' -> '{formateado}'")
    
    print("\n  Limpieza de RUTs:")
    for rut in ruts[:3]:
        limpio = ValidadorRUT.limpiar(rut)
        print(f"    '{rut}' -> '{limpio}'")
    
    print()


def ejemplo_extraccion_partes():
    """Ejemplo 4: Extracción de partes del RUT."""
    print("=" * 60)
    print("EJEMPLO 4: Extracción de Partes del RUT")
    print("=" * 60)
    
    rut = "12.345.678-5"
    partes = ValidadorRUT.extraer_partes(rut)
    
    print(f"\n  RUT: {rut}")
    print(f"  Partes:")
    print(f"    - Número (int):    {partes['numero']}")
    print(f"    - Número (str):    {partes['numero_str']}")
    print(f"    - Dígito Verif.:   {partes['digito_verificador']}")
    print(f"    - RUT Completo:    {partes['rut_completo']}")
    
    print()


def ejemplo_validacion_lista():
    """Ejemplo 5: Validación de lista de RUTs."""
    print("=" * 60)
    print("EJEMPLO 5: Validación de Lista de RUTs")
    print("=" * 60)
    
    ruts = [
        "12.345.678-5",
        "11.111.111-1",
        "12.345.678-0",  # Inválido
        "ABC123",        # Formato inválido
        "22.222.222-2",
        "",              # Vacío
    ]
    
    print(f"\n  RUTs a validar: {len(ruts)}")
    print("-" * 60)
    
    resultados = ValidadorRUT.validar_lista(ruts)
    
    validos = 0
    for r in resultados:
        estado = "✓" if r['es_valido'] else "✗"
        print(f"  {estado} {r['rut_original']:20}", end="")
        
        if r['es_valido']:
            print(f" -> {r['rut_formateado']}")
            validos += 1
        else:
            error_msg = r['error'][:40] + "..." if len(r['error'] or '') > 40 else r['error']
            print(f" -> Error: {error_msg}")
    
    print("-" * 60)
    print(f"  Resumen: {validos}/{len(ruts)} RUTs válidos")
    
    print()


def ejemplo_generacion_ruts_prueba():
    """Ejemplo 6: Generación de RUTs para pruebas."""
    print("=" * 60)
    print("EJEMPLO 6: Generación de RUTs para Pruebas")
    print("=" * 60)
    
    print("\n  ⚠️  ADVERTENCIA: Estos RUTs son solo para pruebas.")
    print("      No corresponden necesariamente a personas reales.\n")
    
    print("  Generando 5 RUTs aleatorios:")
    for i in range(5):
        rut = ValidadorRUT.generar_rut_aleatorio()
        es_valido = ValidadorRUT.validar(rut)
        print(f"    {i+1}. {rut} (válido: {es_valido})")
    
    print("\n  Generando RUTs en rango específico (1M - 5M):")
    for i in range(3):
        rut = ValidadorRUT.generar_rut_aleatorio(minimo=1_000_000, maximo=5_000_000)
        print(f"    {i+1}. {rut}")
    
    print()


def ejemplo_deteccion_empresa():
    """Ejemplo 7: Detección de RUTs de empresa."""
    print("=" * 60)
    print("EJEMPLO 7: Detección de RUTs de Empresa")
    print("=" * 60)
    
    ruts = [
        ("12.345.678-5", "Persona natural"),
        ("76.123.456-7", "Empresa"),
        ("96.000.000-7", "Empresa grande"),
        ("8.765.432-1", "Persona natural"),
    ]
    
    for rut, descripcion in ruts:
        es_empresa = ValidadorRUT.es_rut_empresa(rut)
        tipo = "Empresa" if es_empresa else "Persona"
        print(f"  {rut:20} -> {tipo:10} (esperado: {descripcion})")
    
    print()


def ejemplo_manejo_errores():
    """Ejemplo 8: Manejo de errores."""
    print("=" * 60)
    print("EJEMPLO 8: Manejo de Errores")
    print("=" * 60)
    
    casos_error = [
        "",              # Vacío
        None,            # None
        "ABC",           # Sin dígitos
        "12345",         # Muy corto
        "12.345.678-X",  # Carácter inválido
    ]
    
    for caso in casos_error:
        try:
            resultado = ValidadorRUT.formatear(caso if caso is not None else "")
            print(f"  '{caso}' -> '{resultado}'")
        except RUTInvalidoError as e:
            print(f"  '{caso}' -> RUTInvalidoError: {e.mensaje}")
        except Exception as e:
            print(f"  '{caso}' -> Error inesperado: {e}")
    
    print()


def ejemplo_flask():
    """Ejemplo 9: Uso en Flask (pseudocódigo)."""
    print("=" * 60)
    print("EJEMPLO 9: Uso en Flask")
    print("=" * 60)
    
    print("""
    from flask import Flask, request, jsonify
    from pyrut import ValidadorRUT
    
    app = Flask(__name__)
    
    @app.route('/api/validar-rut', methods=['POST'])
    def validar_rut():
        data = request.json
        rut = data.get('rut', '')
        
        if ValidadorRUT.validar(rut):
            return jsonify({
                'valido': True,
                'rut_formateado': ValidadorRUT.formatear(rut)
            })
        else:
            return jsonify({
                'valido': False,
                'error': 'RUT inválido'
            }), 400
    """)
    print()


def ejemplo_django():
    """Ejemplo 10: Uso en Django (pseudocódigo)."""
    print("=" * 60)
    print("EJEMPLO 10: Uso en Django")
    print("=" * 60)
    
    print("""
    # models.py
    from django.db import models
    from django.core.validators import RegexValidator
    from pyrut import ValidadorRUT
    
    class Persona(models.Model):
        rut = models.CharField(max_length=12, unique=True)
        nombre = models.CharField(max_length=100)
        
        def clean(self):
            if not ValidadorRUT.validar(self.rut):
                raise ValidationError({'rut': 'RUT inválido'})
            # Guardar siempre formateado
            self.rut = ValidadorRUT.formatear(self.rut)
    
    # forms.py
    from django import forms
    from pyrut import ValidadorRUT
    
    class PersonaForm(forms.ModelForm):
        def clean_rut(self):
            rut = self.cleaned_data.get('rut')
            if not ValidadorRUT.validar(rut):
                raise forms.ValidationError('El RUT no es válido')
            return ValidadorRUT.formatear(rut)
    """)
    print()


def main():
    """Ejecuta todos los ejemplos."""
    print("\n" + "=" * 60)
    print("   PyRUT - Ejemplos de Uso")
    print("   Librería de Validación de RUTs Chilenos")
    print("=" * 60 + "\n")
    
    ejemplo_validacion_simple()
    ejemplo_calculo_digito_verificador()
    ejemplo_formateo()
    ejemplo_extraccion_partes()
    ejemplo_validacion_lista()
    ejemplo_generacion_ruts_prueba()
    ejemplo_deteccion_empresa()
    ejemplo_manejo_errores()
    ejemplo_flask()
    ejemplo_django()
    
    print("=" * 60)
    print("   ¡Ejemplos completados!")
    print("=" * 60)


if __name__ == "__main__":
    main()
