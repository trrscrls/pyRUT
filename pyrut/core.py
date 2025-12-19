"""
PyRUT - Librería para validación de RUTs chilenos.

Este módulo contiene la clase principal ValidadorRUT y la excepción RUTInvalidoError
para el manejo de RUTs chilenos (Rol Único Tributario).

Ejemplo de uso:
    >>> from pyrut import ValidadorRUT
    >>> ValidadorRUT.validar("12.345.678-5")
    True
"""

import re
from typing import Optional


class RUTInvalidoError(Exception):
    """Excepción lanzada cuando un RUT es inválido o tiene formato incorrecto.
    
    Attributes:
        mensaje: Descripción del error.
        rut: El RUT que causó el error (si está disponible).
    """
    
    def __init__(self, mensaje: str, rut: Optional[str] = None):
        """Inicializa la excepción con un mensaje y opcionalmente el RUT inválido.
        
        Args:
            mensaje: Descripción del error.
            rut: El RUT que causó el error.
        """
        self.mensaje = mensaje
        self.rut = rut
        super().__init__(f"{mensaje}" + (f" RUT: '{rut}'" if rut else ""))


class ValidadorRUT:
    """Clase para validar, calcular y formatear RUTs chilenos.
    
    Esta clase implementa el algoritmo oficial de módulo 11 utilizado en Chile
    para la validación de RUTs. Todos los métodos son estáticos, por lo que
    no es necesario instanciar la clase.
    
    Formatos aceptados:
        - Con puntos y guión: "12.345.678-9"
        - Solo con guión: "12345678-9"
        - Sin separadores: "123456789"
        - Con 'K' o 'k' como dígito verificador
    
    Example:
        >>> ValidadorRUT.validar("12.345.678-5")
        True
        >>> ValidadorRUT.calcular_digito_verificador(12345678)
        '5'
        >>> ValidadorRUT.formatear("123456785")
        '12.345.678-5'
    """
    
    # Rango aproximado de RUTs válidos en Chile
    RUT_MINIMO: int = 1_000_000
    RUT_MAXIMO: int = 99_999_999
    
    # Patrón para validar formato básico (después de limpiar)
    _PATRON_RUT_LIMPIO = re.compile(r'^(\d{7,8})([0-9Kk])$')
    
    @staticmethod
    def _normalizar_rut(rut: str) -> str:
        """Normaliza un RUT eliminando caracteres no válidos y convirtiendo a mayúsculas.
        
        Args:
            rut: El RUT en cualquier formato.
            
        Returns:
            El RUT limpio (solo números y posiblemente 'K'), en mayúsculas.
            
        Raises:
            RUTInvalidoError: Si el RUT está vacío o es None.
            
        Example:
            >>> ValidadorRUT._normalizar_rut("12.345.678-K")
            '12345678K'
        """
        if rut is None or (isinstance(rut, str) and rut.strip() == ""):
            raise RUTInvalidoError("El RUT no puede estar vacío o ser nulo", rut)
        
        # Eliminar puntos, guiones, espacios y convertir a mayúsculas
        rut_limpio = re.sub(r'[\.\-\s]', '', str(rut).upper().strip())
        
        if not rut_limpio:
            raise RUTInvalidoError("El RUT no puede estar vacío después de limpiar", rut)
            
        return rut_limpio
    
    @staticmethod
    def _algoritmo_modulo11(numero: str) -> str:
        """Calcula el dígito verificador usando el algoritmo módulo 11.
        
        El algoritmo funciona de la siguiente manera:
        1. Se multiplica cada dígito del número (de derecha a izquierda) 
           por la serie cíclica 2, 3, 4, 5, 6, 7.
        2. Se suman todos los productos.
        3. Se calcula el resto de dividir la suma entre 11.
        4. Se resta el resto de 11 para obtener el dígito verificador.
        5. Si el resultado es 11, el dígito es '0'.
        6. Si el resultado es 10, el dígito es 'K'.
        
        Args:
            numero: El número base del RUT como string (sin dígito verificador).
            
        Returns:
            El dígito verificador calculado ('0'-'9' o 'K').
            
        Example:
            >>> ValidadorRUT._algoritmo_modulo11("12345678")
            '5'
        """
        # Serie de multiplicadores (se repite cíclicamente)
        multiplicadores = [2, 3, 4, 5, 6, 7]
        
        # Sumar productos de cada dígito por su multiplicador correspondiente
        suma = 0
        numero_invertido = numero[::-1]  # Invertir para procesar de derecha a izquierda
        
        for i, digito in enumerate(numero_invertido):
            multiplicador = multiplicadores[i % len(multiplicadores)]
            suma += int(digito) * multiplicador
        
        # Calcular el resto y el dígito verificador
        resto = suma % 11
        digito_verificador = 11 - resto
        
        # Casos especiales
        if digito_verificador == 11:
            return '0'
        elif digito_verificador == 10:
            return 'K'
        else:
            return str(digito_verificador)
    
    @classmethod
    def limpiar(cls, rut: str) -> str:
        """Elimina puntos, guiones y espacios de un RUT.
        
        Args:
            rut: El RUT en cualquier formato.
            
        Returns:
            El RUT sin puntos, guiones ni espacios, en mayúsculas.
            
        Raises:
            RUTInvalidoError: Si el RUT está vacío o es None.
            
        Example:
            >>> ValidadorRUT.limpiar("12.345.678-K")
            '12345678K'
            >>> ValidadorRUT.limpiar("12345678-9")
            '123456789'
        """
        return cls._normalizar_rut(rut)
    
    @classmethod
    def extraer_partes(cls, rut: str) -> dict:
        """Extrae el número base y el dígito verificador de un RUT.
        
        Args:
            rut: El RUT en cualquier formato válido.
            
        Returns:
            Un diccionario con las claves:
                - 'numero': El número base como int.
                - 'numero_str': El número base como string.
                - 'digito_verificador': El dígito verificador como string.
                - 'rut_completo': El RUT completo limpio.
                
        Raises:
            RUTInvalidoError: Si el RUT tiene formato inválido.
            
        Example:
            >>> ValidadorRUT.extraer_partes("12.345.678-K")
            {'numero': 12345678, 'numero_str': '12345678', 
             'digito_verificador': 'K', 'rut_completo': '12345678K'}
        """
        rut_limpio = cls._normalizar_rut(rut)
        
        # Validar formato básico
        match = cls._PATRON_RUT_LIMPIO.match(rut_limpio)
        if not match:
            raise RUTInvalidoError(
                "Formato de RUT inválido. Debe tener 7-8 dígitos más dígito verificador",
                rut
            )
        
        numero_str = match.group(1)
        digito_verificador = match.group(2).upper()
        
        return {
            'numero': int(numero_str),
            'numero_str': numero_str,
            'digito_verificador': digito_verificador,
            'rut_completo': rut_limpio
        }
    
    @classmethod
    def calcular_digito_verificador(cls, numero: int) -> str:
        """Calcula el dígito verificador para un número de RUT dado.
        
        Args:
            numero: El número base del RUT (sin dígito verificador).
                   Debe ser un entero positivo.
                   
        Returns:
            El dígito verificador calculado ('0'-'9' o 'K').
            
        Raises:
            RUTInvalidoError: Si el número es inválido (negativo, cero, 
                             o fuera de rango razonable).
                             
        Example:
            >>> ValidadorRUT.calcular_digito_verificador(12345678)
            '5'
            >>> ValidadorRUT.calcular_digito_verificador(11111111)
            '1'
        """
        if not isinstance(numero, int):
            try:
                numero = int(numero)
            except (ValueError, TypeError):
                raise RUTInvalidoError(
                    f"El número debe ser un entero válido, se recibió: {type(numero).__name__}"
                )
        
        if numero <= 0:
            raise RUTInvalidoError("El número del RUT debe ser positivo", str(numero))
        
        return cls._algoritmo_modulo11(str(numero))
    
    @classmethod
    def validar(cls, rut: str, verificar_rango: bool = False) -> bool:
        """Valida si un RUT chileno es válido.
        
        Verifica que el formato sea correcto y que el dígito verificador
        corresponda al número base según el algoritmo módulo 11.
        
        Args:
            rut: El RUT a validar en cualquier formato aceptado.
            verificar_rango: Si es True, también verifica que el número
                            esté dentro del rango típico de RUTs chilenos
                            (1.000.000 - 99.999.999). Por defecto es False.
                            
        Returns:
            True si el RUT es válido, False en caso contrario.
            
        Example:
            >>> ValidadorRUT.validar("12.345.678-5")
            True
            >>> ValidadorRUT.validar("12345678-5")
            True
            >>> ValidadorRUT.validar("123456785")
            True
            >>> ValidadorRUT.validar("12.345.678-0")  # Dígito incorrecto
            False
        """
        try:
            partes = cls.extraer_partes(rut)
            numero_str = partes['numero_str']
            digito_proporcionado = partes['digito_verificador']
            numero = partes['numero']
            
            # Verificar rango si se solicita
            if verificar_rango:
                if numero < cls.RUT_MINIMO or numero > cls.RUT_MAXIMO:
                    return False
            
            # Calcular dígito verificador esperado
            digito_calculado = cls._algoritmo_modulo11(numero_str)
            
            # Comparar (case-insensitive ya que normalizamos a mayúsculas)
            return digito_proporcionado == digito_calculado
            
        except RUTInvalidoError:
            return False
    
    @classmethod
    def formatear(cls, rut: str, con_puntos: bool = True) -> str:
        """Formatea un RUT al formato estándar chileno.
        
        Args:
            rut: El RUT en cualquier formato válido.
            con_puntos: Si es True, incluye puntos de miles (12.345.678-9).
                       Si es False, solo incluye el guión (12345678-9).
                       Por defecto es True.
                       
        Returns:
            El RUT formateado correctamente.
            
        Raises:
            RUTInvalidoError: Si el RUT tiene formato inválido.
            
        Example:
            >>> ValidadorRUT.formatear("123456785")
            '12.345.678-5'
            >>> ValidadorRUT.formatear("123456785", con_puntos=False)
            '12345678-5'
        """
        partes = cls.extraer_partes(rut)
        numero_str = partes['numero_str']
        digito = partes['digito_verificador']
        
        if con_puntos:
            # Formatear con puntos de miles
            numero_formateado = ""
            for i, char in enumerate(reversed(numero_str)):
                if i > 0 and i % 3 == 0:
                    numero_formateado = "." + numero_formateado
                numero_formateado = char + numero_formateado
            return f"{numero_formateado}-{digito}"
        else:
            return f"{numero_str}-{digito}"
    
    @classmethod
    def validar_lista(cls, ruts: list, verificar_rango: bool = False) -> list:
        """Valida una lista de RUTs y retorna resultados detallados.
        
        Args:
            ruts: Lista de RUTs a validar (en cualquier formato).
            verificar_rango: Si es True, también verifica el rango de cada RUT.
            
        Returns:
            Lista de diccionarios, cada uno con:
                - 'rut_original': El RUT tal como fue proporcionado.
                - 'rut_formateado': El RUT formateado (si es válido) o None.
                - 'es_valido': True si el RUT es válido, False en caso contrario.
                - 'error': Mensaje de error si el RUT es inválido, None si es válido.
                
        Example:
            >>> resultados = ValidadorRUT.validar_lista([
            ...     "12.345.678-5",
            ...     "11.111.111-0",
            ...     "invalido"
            ... ])
            >>> resultados[0]['es_valido']
            True
        """
        resultados = []
        
        for rut in ruts:
            resultado = {
                'rut_original': rut,
                'rut_formateado': None,
                'es_valido': False,
                'error': None
            }
            
            try:
                es_valido = cls.validar(rut, verificar_rango=verificar_rango)
                resultado['es_valido'] = es_valido
                
                if es_valido:
                    resultado['rut_formateado'] = cls.formatear(rut)
                else:
                    # Intentar dar más información sobre por qué es inválido
                    try:
                        partes = cls.extraer_partes(rut)
                        digito_correcto = cls.calcular_digito_verificador(partes['numero'])
                        resultado['error'] = (
                            f"Dígito verificador incorrecto. "
                            f"Esperado: '{digito_correcto}', "
                            f"Proporcionado: '{partes['digito_verificador']}'"
                        )
                    except RUTInvalidoError as e:
                        resultado['error'] = str(e)
                        
            except Exception as e:
                resultado['error'] = str(e)
            
            resultados.append(resultado)
        
        return resultados
    
    @classmethod
    def generar_rut_aleatorio(cls, minimo: int = 10_000_000, maximo: int = 25_000_000) -> str:
        """Genera un RUT válido aleatorio para pruebas.
        
        ADVERTENCIA: Este método es solo para pruebas y desarrollo.
        Los RUTs generados son matemáticamente válidos pero no corresponden
        necesariamente a personas reales.
        
        Args:
            minimo: Número mínimo del RUT a generar.
            maximo: Número máximo del RUT a generar.
            
        Returns:
            Un RUT válido formateado con puntos y guión.
            
        Example:
            >>> rut = ValidadorRUT.generar_rut_aleatorio()
            >>> ValidadorRUT.validar(rut)
            True
        """
        import random
        numero = random.randint(minimo, maximo)
        digito = cls.calcular_digito_verificador(numero)
        return cls.formatear(f"{numero}{digito}")
    
    @classmethod
    def es_rut_empresa(cls, rut: str) -> bool:
        """Determina si un RUT corresponde probablemente a una empresa.
        
        En Chile, los RUTs de empresas generalmente comienzan con números
        más altos (típicamente 50.000.000 o más), aunque esto no es una
        regla absoluta.
        
        Args:
            rut: El RUT a verificar.
            
        Returns:
            True si el RUT probablemente corresponde a una empresa.
            
        Note:
            Esta es una heurística aproximada, no una regla oficial.
            
        Example:
            >>> ValidadorRUT.es_rut_empresa("76.123.456-7")
            True
            >>> ValidadorRUT.es_rut_empresa("12.345.678-5")
            False
        """
        try:
            partes = cls.extraer_partes(rut)
            # RUTs de empresas típicamente empiezan con 50+ millones
            return partes['numero'] >= 50_000_000
        except RUTInvalidoError:
            return False
