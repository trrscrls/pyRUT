"""
Tests unitarios para PyRUT - Librería de validación de RUTs chilenos.

Ejecutar con: pytest tests/test_validador.py -v
"""

import pytest
from pyrut import ValidadorRUT, RUTInvalidoError


class TestValidarRUT:
    """Tests para el método validar()."""
    
    def test_validar_rut_correcto_con_puntos(self):
        """Valida un RUT correcto con formato completo (puntos y guión)."""
        assert ValidadorRUT.validar("12.345.678-5") is True
    
    def test_validar_rut_correcto_sin_puntos(self):
        """Valida un RUT correcto solo con guión."""
        assert ValidadorRUT.validar("12345678-5") is True
    
    def test_validar_rut_correcto_sin_separadores(self):
        """Valida un RUT correcto sin ningún separador."""
        assert ValidadorRUT.validar("123456785") is True
    
    def test_validar_rut_con_k_mayuscula(self):
        """Valida un RUT con dígito verificador K mayúscula."""
        # 9.007.890-K es un RUT válido
        assert ValidadorRUT.validar("9.007.890-K") is True
    
    def test_validar_rut_con_k_minuscula(self):
        """Valida un RUT con dígito verificador k minúscula."""
        assert ValidadorRUT.validar("9.007.890-k") is True
    
    def test_validar_rut_incorrecto(self):
        """Rechaza un RUT con dígito verificador incorrecto."""
        assert ValidadorRUT.validar("12.345.678-0") is False
    
    def test_validar_rut_muy_corto(self):
        """Rechaza un RUT con menos dígitos de los necesarios."""
        assert ValidadorRUT.validar("12345-5") is False
    
    def test_validar_rut_vacio(self):
        """Rechaza un RUT vacío."""
        assert ValidadorRUT.validar("") is False
    
    def test_validar_rut_con_letras(self):
        """Rechaza un RUT con caracteres no válidos."""
        assert ValidadorRUT.validar("ABC12345-5") is False
    
    def test_validar_rut_11111111_1(self):
        """Valida el RUT 11.111.111-1."""
        assert ValidadorRUT.validar("11.111.111-1") is True
    
    def test_validar_rut_22222222_2(self):
        """Valida el RUT 22.222.222-2."""
        assert ValidadorRUT.validar("22.222.222-2") is True
    
    def test_validar_con_verificacion_rango_valido(self):
        """Valida RUT dentro del rango típico."""
        assert ValidadorRUT.validar("12.345.678-5", verificar_rango=True) is True
    
    def test_validar_con_verificacion_rango_bajo(self):
        """Rechaza RUT por debajo del rango mínimo."""
        # Crear un RUT válido con número muy bajo
        digito = ValidadorRUT.calcular_digito_verificador(100)
        assert ValidadorRUT.validar(f"100-{digito}", verificar_rango=True) is False


class TestCalcularDigitoVerificador:
    """Tests para el método calcular_digito_verificador()."""
    
    def test_calcular_dv_12345678(self):
        """Calcula el DV para 12345678 (debe ser 5)."""
        assert ValidadorRUT.calcular_digito_verificador(12345678) == "5"
    
    def test_calcular_dv_11111111(self):
        """Calcula el DV para 11111111 (debe ser 1)."""
        assert ValidadorRUT.calcular_digito_verificador(11111111) == "1"
    
    def test_calcular_dv_22222222(self):
        """Calcula el DV para 22222222 (debe ser 2)."""
        assert ValidadorRUT.calcular_digito_verificador(22222222) == "2"
    
    def test_calcular_dv_con_k(self):
        """Calcula el DV que resulta en K."""
        assert ValidadorRUT.calcular_digito_verificador(9007890) == "K"
    
    def test_calcular_dv_con_cero(self):
        """Calcula el DV que resulta en 0."""
        # Buscar un número cuyo DV sea 0
        assert ValidadorRUT.calcular_digito_verificador(11111112) == "0"
    
    def test_calcular_dv_numero_string(self):
        """Acepta número como string."""
        assert ValidadorRUT.calcular_digito_verificador(12345678) == "5"
    
    def test_calcular_dv_numero_negativo_error(self):
        """Lanza error con número negativo."""
        with pytest.raises(RUTInvalidoError):
            ValidadorRUT.calcular_digito_verificador(-12345678)
    
    def test_calcular_dv_cero_error(self):
        """Lanza error con número cero."""
        with pytest.raises(RUTInvalidoError):
            ValidadorRUT.calcular_digito_verificador(0)


class TestFormatear:
    """Tests para el método formatear()."""
    
    def test_formatear_con_puntos(self):
        """Formatea RUT con puntos y guión."""
        assert ValidadorRUT.formatear("123456785") == "12.345.678-5"
    
    def test_formatear_sin_puntos(self):
        """Formatea RUT solo con guión."""
        assert ValidadorRUT.formatear("123456785", con_puntos=False) == "12345678-5"
    
    def test_formatear_desde_formato_completo(self):
        """Reformatea RUT ya formateado."""
        assert ValidadorRUT.formatear("12.345.678-5") == "12.345.678-5"
    
    def test_formatear_con_k(self):
        """Formatea RUT con dígito K."""
        assert ValidadorRUT.formatear("9007890K") == "9.007.890-K"
    
    def test_formatear_con_k_minuscula(self):
        """Formatea RUT con dígito k minúscula (se convierte a mayúscula)."""
        resultado = ValidadorRUT.formatear("9007890k")
        assert resultado == "9.007.890-K"
    
    def test_formatear_rut_corto(self):
        """Formatea RUT con menos de 8 dígitos."""
        assert ValidadorRUT.formatear("1234567-K") == "1.234.567-K"
    
    def test_formatear_rut_vacio_error(self):
        """Lanza error al formatear RUT vacío."""
        with pytest.raises(RUTInvalidoError):
            ValidadorRUT.formatear("")


class TestLimpiar:
    """Tests para el método limpiar()."""
    
    def test_limpiar_con_puntos_y_guion(self):
        """Limpia RUT con puntos y guión."""
        assert ValidadorRUT.limpiar("12.345.678-5") == "123456785"
    
    def test_limpiar_con_espacios(self):
        """Limpia RUT con espacios."""
        assert ValidadorRUT.limpiar("  12.345.678-5  ") == "123456785"
    
    def test_limpiar_ya_limpio(self):
        """Limpia RUT que ya está limpio."""
        assert ValidadorRUT.limpiar("123456785") == "123456785"
    
    def test_limpiar_con_k_minuscula(self):
        """Limpia RUT con k minúscula (se convierte a mayúscula)."""
        assert ValidadorRUT.limpiar("9.007.890-k") == "9007890K"
    
    def test_limpiar_vacio_error(self):
        """Lanza error al limpiar RUT vacío."""
        with pytest.raises(RUTInvalidoError):
            ValidadorRUT.limpiar("")


class TestExtraerPartes:
    """Tests para el método extraer_partes()."""
    
    def test_extraer_partes_rut_completo(self):
        """Extrae partes de un RUT completo."""
        partes = ValidadorRUT.extraer_partes("12.345.678-5")
        assert partes['numero'] == 12345678
        assert partes['numero_str'] == "12345678"
        assert partes['digito_verificador'] == "5"
        assert partes['rut_completo'] == "123456785"
    
    def test_extraer_partes_con_k(self):
        """Extrae partes de un RUT con K."""
        partes = ValidadorRUT.extraer_partes("9.007.890-K")
        assert partes['digito_verificador'] == "K"
    
    def test_extraer_partes_formato_invalido_error(self):
        """Lanza error con formato inválido."""
        with pytest.raises(RUTInvalidoError):
            ValidadorRUT.extraer_partes("ABC123")


class TestValidarLista:
    """Tests para el método validar_lista()."""
    
    def test_validar_lista_mixta(self):
        """Valida una lista con RUTs válidos e inválidos."""
        ruts = ["12.345.678-5", "12.345.678-0", "invalido"]
        resultados = ValidadorRUT.validar_lista(ruts)
        
        assert len(resultados) == 3
        assert resultados[0]['es_valido'] is True
        assert resultados[1]['es_valido'] is False
        assert resultados[2]['es_valido'] is False
    
    def test_validar_lista_todos_validos(self):
        """Valida una lista donde todos son válidos."""
        ruts = ["12.345.678-5", "11.111.111-1", "22.222.222-2"]
        resultados = ValidadorRUT.validar_lista(ruts)
        
        todos_validos = all(r['es_valido'] for r in resultados)
        assert todos_validos is True
    
    def test_validar_lista_vacia(self):
        """Valida una lista vacía."""
        resultados = ValidadorRUT.validar_lista([])
        assert resultados == []
    
    def test_validar_lista_incluye_formateado(self):
        """Verifica que los válidos incluyan formato correcto."""
        ruts = ["123456785"]
        resultados = ValidadorRUT.validar_lista(ruts)
        
        assert resultados[0]['rut_formateado'] == "12.345.678-5"


class TestGenerarRutAleatorio:
    """Tests para el método generar_rut_aleatorio()."""
    
    def test_generar_rut_valido(self):
        """Genera un RUT que sea válido."""
        rut = ValidadorRUT.generar_rut_aleatorio()
        assert ValidadorRUT.validar(rut) is True
    
    def test_generar_rut_formateado(self):
        """Genera un RUT con formato correcto."""
        rut = ValidadorRUT.generar_rut_aleatorio()
        assert "." in rut
        assert "-" in rut
    
    def test_generar_rut_rango_especifico(self):
        """Genera RUTs dentro de un rango específico."""
        for _ in range(10):
            rut = ValidadorRUT.generar_rut_aleatorio(minimo=10_000_000, maximo=11_000_000)
            partes = ValidadorRUT.extraer_partes(rut)
            assert 10_000_000 <= partes['numero'] <= 11_000_000


class TestEsRutEmpresa:
    """Tests para el método es_rut_empresa()."""
    
    def test_es_rut_empresa_verdadero(self):
        """Detecta RUT de empresa (>= 50M)."""
        # Generar un RUT de empresa válido
        digito = ValidadorRUT.calcular_digito_verificador(76123456)
        rut = f"76.123.456-{digito}"
        assert ValidadorRUT.es_rut_empresa(rut) is True
    
    def test_es_rut_empresa_falso(self):
        """Detecta RUT de persona (< 50M)."""
        assert ValidadorRUT.es_rut_empresa("12.345.678-5") is False
    
    def test_es_rut_empresa_invalido(self):
        """Retorna False para RUT inválido."""
        assert ValidadorRUT.es_rut_empresa("invalido") is False


class TestCasosLimite:
    """Tests para casos límite y especiales."""
    
    def test_rut_con_ceros_izquierda(self):
        """Valida RUT que podría tener ceros a la izquierda."""
        # RUT con 7 dígitos (implícitamente un cero a la izquierda)
        digito = ValidadorRUT.calcular_digito_verificador(1234567)
        rut = f"1.234.567-{digito}"
        assert ValidadorRUT.validar(rut) is True
    
    def test_rut_minimo_posible(self):
        """Valida el RUT más pequeño posible."""
        digito = ValidadorRUT.calcular_digito_verificador(1000000)
        rut = f"1000000{digito}"
        assert ValidadorRUT.validar(rut) is True
    
    def test_rut_maximo_posible(self):
        """Valida un RUT muy grande."""
        digito = ValidadorRUT.calcular_digito_verificador(99999999)
        rut = f"99999999{digito}"
        assert ValidadorRUT.validar(rut) is True
    
    def test_rut_con_muchos_espacios(self):
        """Valida RUT con muchos espacios."""
        assert ValidadorRUT.validar("  12.345.678-5  ") is True
    
    def test_none_como_entrada(self):
        """Maneja None como entrada."""
        assert ValidadorRUT.validar(None) is False


class TestRUTInvalidoError:
    """Tests para la excepción RUTInvalidoError."""
    
    def test_excepcion_con_mensaje(self):
        """Verifica que la excepción contenga el mensaje."""
        try:
            raise RUTInvalidoError("Test de error")
        except RUTInvalidoError as e:
            assert e.mensaje == "Test de error"
            assert e.rut is None
    
    def test_excepcion_con_rut(self):
        """Verifica que la excepción contenga el RUT."""
        try:
            raise RUTInvalidoError("Test de error", "12345")
        except RUTInvalidoError as e:
            assert e.rut == "12345"
            assert "12345" in str(e)


# Tests de integración
class TestIntegracion:
    """Tests de integración que combinan múltiples operaciones."""
    
    def test_flujo_completo_validacion(self):
        """Test de flujo completo: limpiar -> validar -> formatear."""
        rut_entrada = "  12.345.678-5  "
        
        # Limpiar
        rut_limpio = ValidadorRUT.limpiar(rut_entrada)
        assert rut_limpio == "123456785"
        
        # Validar
        assert ValidadorRUT.validar(rut_limpio) is True
        
        # Formatear
        rut_formateado = ValidadorRUT.formatear(rut_limpio)
        assert rut_formateado == "12.345.678-5"
    
    def test_calcular_y_validar(self):
        """Test de calcular DV y validar el RUT resultante."""
        numero = 18885542
        digito = ValidadorRUT.calcular_digito_verificador(numero)
        rut_completo = f"{numero}{digito}"
        
        assert ValidadorRUT.validar(rut_completo) is True
    
    def test_generar_y_extraer(self):
        """Test de generar RUT y extraer sus partes."""
        rut = ValidadorRUT.generar_rut_aleatorio()
        partes = ValidadorRUT.extraer_partes(rut)
        
        # Verificar que el DV es correcto
        dv_calculado = ValidadorRUT.calcular_digito_verificador(partes['numero'])
        assert partes['digito_verificador'] == dv_calculado


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
