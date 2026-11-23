# Control de gastos personales

## Objetivo

Aplicación web ligera con Flask para registrar gastos personales con fecha y categoría, validar montos positivos y calcular el total. La versión web mantiene los gastos en memoria; reiniciar el proceso limpia la lista. El proyecto sirve para practicar control de versiones, pruebas automatizadas, integración continua y despliegue.

## Herramientas

- Python 3.12 o posterior
- Flask (framework web)
- CSS puro integrado
- Gunicorn
- Git
- GitHub
- GitHub Actions
- Pruebas con `unittest` (incluido en Python)

## Estructura

```text
.
├── .github/
│   └── workflows/
│       └── ci.yml
├── templates/
│   └── index.html
├── tests/
│   └── test_control_gastos.py
├── .gitignore
├── app.py
├── control_gastos.py
├── performance_test.py
├── requirements.txt
├── ENTREGA_SEMANA1.md
└── README.md
```

## Ejecutar el programa

### Opción 1: Aplicación web (recomendada)

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Ejecutar el servidor Flask:
```bash
python app.py
```

3. Abrir el navegador en `http://localhost:5000`

La aplicación web permite:
- Agregar gastos mediante un formulario
- Ver la lista de gastos en una tabla
- Consultar el contador y el total acumulado
- Reiniciar rápidamente la lista con el botón `Limpiar lista`
- Los gastos web viven únicamente en memoria

También está disponible el monitoreo básico:

```bash
curl http://localhost:5000/health
```

### Opción 2: Aplicación de consola

Desde esta carpeta, ejecuta:

```bash
python control_gastos.py
```

El programa carga automáticamente los gastos guardados en `gastos.json` si existe. Luego:

1. Escribe la descripción del gasto
2. Selecciona una categoría (Comida, Transporte, Vivienda, Entretenimiento, Salud, Otros)
3. Ingresa el monto
4. Para terminar, deja vacía la descripción

Al final, el programa muestra todos los gastos con su fecha y categoría, el total acumulado, y pregunta si deseas guardar los cambios en `gastos.json`.

## Ejecutar las pruebas

```bash
python -m unittest discover -s tests -v
```

## Prueba de carga

Con el servidor ejecutándose en otra terminal:

```bash
python performance_test.py
```

Para probar una URL desplegada:

```bash
python performance_test.py https://tu-servicio.onrender.com/health
```

El script ejecuta 50 solicitudes concurrentes y muestra los tiempos promedio, mínimo y máximo.

## Integración continua

El flujo de GitHub Actions está en `.github/workflows/ci.yml`. Se ejecuta en cada `push` y en cada `pull_request`; prepara Python 3.12, instala `requirements.txt` y corre las pruebas de `unittest`. Un resultado exitoso significa que todas las pruebas terminaron sin errores.

## Despliegue en Render

Crea un servicio web desde el repositorio y configura el comando de compilación como `pip install -r requirements.txt` y el comando de inicio como `gunicorn app:app`. La versión web usa memoria; al reiniciar el servicio, la lista se vacía. Para persistencia permanente se debe integrar posteriormente almacenamiento persistente o una base de datos.

## Git y GitHub

El proyecto está publicado en [github.com/mainsionxd-coder/kalebEntregas](https://github.com/mainsionxd-coder/kalebEntregas). Para obtener una copia:

```bash
git clone https://github.com/mainsionxd-coder/kalebEntregas.git
```

Los cambios se registran con commits descriptivos y se publican con `git push`. La guía de la entrega y las evidencias que debes capturar están en `ENTREGA_SEMANA1.md`.
