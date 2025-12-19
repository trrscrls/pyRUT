"""
Ejemplos de uso de PyRUT - Librería de validación de RUTs/RUNs chilenos.

Para ejecutar: python examples/ejemplo_uso.py
"""

from pyrut import ValidadorRUT, ValidadorRUN, RUTInvalidoError


def main():
    print("=" * 60)
    print("   PyRUT - Ejemplos de Uso")
    print("=" * 60)
    
    # Ejemplo 1: Validación simple
    print("\n1. VALIDACIÓN SIMPLE")
    ruts = ["12.345.678-5", "12345678-5", "123456785", "12.345.678-0"]
    for rut in ruts:
        estado = "✓ Válido" if ValidadorRUT.validar(rut) else "✗ Inválido"
        print(f"   {rut:20} -> {estado}")
    
    # Ejemplo 2: Calcular dígito verificador
    print("\n2. CALCULAR DÍGITO VERIFICADOR")
    numeros = [12345678, 11111111, 9007890]
    for num in numeros:
        dv = ValidadorRUT.calcular_digito_verificador(num)
        print(f"   {num:,} -> Dígito: {dv}")
    
    # Ejemplo 3: Formatear
    print("\n3. FORMATEAR RUT")
    print(f"   '123456785' -> '{ValidadorRUT.formatear('123456785')}'")
    print(f"   '123456785' (sin puntos) -> '{ValidadorRUT.formatear('123456785', con_puntos=False)}'")
    
    # Ejemplo 4: Limpiar
    print("\n4. LIMPIAR RUT")
    print(f"   '12.345.678-5' -> '{ValidadorRUT.limpiar('12.345.678-5')}'")
    
    # Ejemplo 5: Extraer partes
    print("\n5. EXTRAER PARTES")
    partes = ValidadorRUT.extraer_partes("12.345.678-5")
    print(f"   Número: {partes['numero']}, DV: {partes['digito_verificador']}")
    
    # Ejemplo 6: ValidadorRUN (alias)
    print("\n6. VALIDADOR RUN (alias)")
    print(f"   ValidadorRUN.validar('12.345.678-5') -> {ValidadorRUN.validar('12.345.678-5')}")
    
    # Ejemplo 7: Validar lista
    print("\n7. VALIDAR LISTA")
    resultados = ValidadorRUT.validar_lista(["12.345.678-5", "11.111.111-0"])
    for r in resultados:
        estado = "✓" if r['es_valido'] else "✗"
        print(f"   {estado} {r['rut_original']}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
