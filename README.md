# PyRUT 🇨🇱

Librería Python para validación de **RUTs** y **RUNs** chilenos.

> **Nota:** En Chile, el RUT (Rol Único Tributario) y el RUN (Rol Único Nacional) 
> usan el mismo formato y algoritmo de validación (módulo 11). Esta librería 
> funciona para ambos.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Características

- ✅ **Validación completa** de RUTs con algoritmo módulo 11
- 🔢 **Cálculo de dígito verificador** a partir del número base
- 📝 **Formateo flexible** (con/sin puntos)
- 🧹 **Limpieza y normalización** de RUTs
- 📋 **Validación de listas** de RUTs
- 🔤 Manejo de **'K' como dígito verificador**
- 📦 **Sin dependencias externas**
- 🐍 Compatible con **Python 3.8+**

## 📦 Instalación

### Desde pip (cuando esté publicado)

```bash
pip install pyrut
```

### Desde el código fuente

```bash
git clone https://github.com/tu-usuario/pyrut.git
cd pyrut
pip install -e .
```

### Dependencias de desarrollo

```bash
pip install -r requirements.txt
```

## 🚀 Uso Básico

### Importar la librería

```python
from pyrut import ValidadorRUT, RUTInvalidoError
```

### Validar un RUT

```python
# Todos estos formatos son válidos
ValidadorRUT.validar("12.345.678-5")  # True
ValidadorRUT.validar("12345678-5")    # True
ValidadorRUT.validar("123456785")     # True
ValidadorRUT.validar("12.345.678-K")  # True (si K es correcto)

# RUT inválido
ValidadorRUT.validar("12.345.678-0")  # False (dígito incorrecto)
```

### Calcular dígito verificador

```python
# A partir de un número
ValidadorRUT.calcular_digito_verificador(12345678)  # '5'
ValidadorRUT.calcular_digito_verificador(11111111)  # '1'
ValidadorRUT.calcular_digito_verificador(22222222)  # '2'
```

### Formatear un RUT

```python
# Con puntos (default)
ValidadorRUT.formatear("123456785")  # '12.345.678-5'

# Sin puntos
ValidadorRUT.formatear("123456785", con_puntos=False)  # '12345678-5'

# Limpiar formato existente y reformatear
ValidadorRUT.formatear("12.345.678-5", con_puntos=True)  # '12.345.678-5'
```

### Limpiar un RUT

```python
ValidadorRUT.limpiar("12.345.678-5")  # '123456785'
ValidadorRUT.limpiar("12345678-K")    # '12345678K'
```

### Extraer partes del RUT

```python
partes = ValidadorRUT.extraer_partes("12.345.678-5")
print(partes)
# {
#     'numero': 12345678,
#     'numero_str': '12345678',
#     'digito_verificador': '5',
#     'rut_completo': '123456785'
# }
```

### Validar lista de RUTs

```python
ruts = ["12.345.678-5", "11.111.111-0", "invalido"]
resultados = ValidadorRUT.validar_lista(ruts)

for r in resultados:
    print(f"{r['rut_original']}: {'✓' if r['es_valido'] else '✗'}")
    if r['error']:
        print(f"  Error: {r['error']}")
```

### Generar RUT aleatorio (para testing)

```python
rut = ValidadorRUT.generar_rut_aleatorio()
print(rut)  # Ej: '15.432.876-3'
print(ValidadorRUT.validar(rut))  # True
```

## 📖 API Reference

### Clase `ValidadorRUT`

Todos los métodos son **estáticos o de clase**, no es necesario instanciar.

| Método | Descripción | Retorno |
|--------|-------------|---------|
| `validar(rut, verificar_rango=False)` | Valida si un RUT es válido | `bool` |
| `calcular_digito_verificador(numero)` | Calcula el DV de un número | `str` |
| `formatear(rut, con_puntos=True)` | Formatea un RUT | `str` |
| `limpiar(rut)` | Elimina puntos y guiones | `str` |
| `extraer_partes(rut)` | Extrae número y DV | `dict` |
| `validar_lista(ruts)` | Valida múltiples RUTs | `list[dict]` |
| `generar_rut_aleatorio(min, max)` | Genera RUT de prueba | `str` |
| `es_rut_empresa(rut)` | Indica si es RUT de empresa | `bool` |

### Excepción `RUTInvalidoError`

Se lanza cuando un RUT tiene formato inválido o está vacío.

```python
from pyrut import ValidadorRUT, RUTInvalidoError

try:
    ValidadorRUT.formatear("")  # RUT vacío
except RUTInvalidoError as e:
    print(f"Error: {e.mensaje}")
    print(f"RUT problemático: {e.rut}")
```

## 🧮 Algoritmo de Validación (Módulo 11)

El RUT chileno se valida usando el "Módulo 11":

1. **Separar** el número base del dígito verificador
2. **Multiplicar** cada dígito del número (de derecha a izquierda) por la serie `2, 3, 4, 5, 6, 7` (cíclica)
3. **Sumar** todos los productos
4. **Calcular** el resto de dividir la suma entre 11
5. **Restar** el resto de 11 para obtener el dígito verificador
6. **Casos especiales**: Si el resultado es 11 → `"0"`, si es 10 → `"K"`

### Ejemplo paso a paso

```
RUT a validar: 12.345.678-5

1. Número base: 12345678

2. Multiplicación (derecha a izquierda):
   Dígito:        8   7   6   5   4   3   2   1
   Multiplicador: 2   3   4   5   6   7   2   3
   Producto:     16  21  24  25  24  21   4   3

3. Suma: 16 + 21 + 24 + 25 + 24 + 21 + 4 + 3 = 138

4. Resto: 138 % 11 = 6

5. Dígito verificador: 11 - 6 = 5

✓ El dígito verificador es 5, el RUT es válido.
```

## 📊 Ejemplos de RUTs

### RUTs válidos

| RUT | Dígito Verificador |
|-----|-------------------|
| 12.345.678-5 | 5 |
| 11.111.111-1 | 1 |
| 22.222.222-2 | 2 |
| 33.333.333-3 | 3 |
| 9.007.890-K | K |

### RUTs inválidos

| RUT | Problema |
|-----|----------|
| 12.345.678-0 | DV incorrecto (debería ser 5) |
| 12345 | Muy corto |
| 12.345.678-X | Carácter inválido |
| | Vacío |

## 🌐 Uso en Aplicaciones Web

### Flask

```python
from flask import Flask, request, jsonify
from pyrut import ValidadorRUT

app = Flask(__name__)

@app.route('/validar-rut', methods=['POST'])
def validar_rut():
    rut = request.json.get('rut', '')
    
    es_valido = ValidadorRUT.validar(rut)
    
    return jsonify({
        'rut': rut,
        'valido': es_valido,
        'formateado': ValidadorRUT.formatear(rut) if es_valido else None
    })
```

### Django

```python
# forms.py
from django import forms
from pyrut import ValidadorRUT

class PersonaForm(forms.Form):
    rut = forms.CharField(max_length=12)
    
    def clean_rut(self):
        rut = self.cleaned_data['rut']
        if not ValidadorRUT.validar(rut):
            raise forms.ValidationError('El RUT ingresado no es válido')
        return ValidadorRUT.formatear(rut)
```

```python
# validators.py
from django.core.exceptions import ValidationError
from pyrut import ValidadorRUT

def validar_rut(value):
    if not ValidadorRUT.validar(value):
        raise ValidationError(
            '%(value)s no es un RUT válido',
            params={'value': value},
        )
```

## 🧪 Testing

### Ejecutar tests

```bash
# Todos los tests
pytest tests/ -v

# Con cobertura
pytest tests/ -v --cov=pyrut

# Test específico
pytest tests/test_validador.py::test_validar_rut_correcto -v
```

## 📝 Notas Importantes

### Rango de RUTs válidos

- Los RUTs de personas en Chile típicamente están entre **1.000.000** y **25.000.000**
- Los RUTs de empresas generalmente son **50.000.000+**
- Use `verificar_rango=True` para validar el rango

### Dígito verificador 'K'

- El dígito 'K' equivale a 10 en el algoritmo
- La librería acepta tanto 'K' mayúscula como 'k' minúscula
- Internamente se normaliza a 'K' mayúscula

### Ceros a la izquierda

- Los RUTs pueden tener ceros a la izquierda: `01.234.567-8`
- La librería los maneja correctamente

## 📄 Licencia

MIT License

Copyright (c) 2024 PyRUT Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📞 Soporte

Si encuentras un bug o tienes una sugerencia, por favor abre un [issue](https://github.com/tu-usuario/pyrut/issues).
