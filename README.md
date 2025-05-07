# E-commerce con Django

Un sistema de e-commerce básico desarrollado con Django.

## Características

- Registro y login de usuarios
- Catálogo de productos
- Sistema de carrito de compras
- Checkout con dirección de envío
- Preparado para integración con Transbank WebPay Plus

## Requisitos

- Python 3.8+
- Django 5.0+
- Pillow
- django-crispy-forms
- crispy-bootstrap5

## Instalación

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd ecommerce
```

2. Crear y activar un entorno virtual:
```bash
python -m venv venv
venv\Scripts\activate  # En Windows
source venv/bin/activate  # En Linux/Mac
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Realizar migraciones:
```bash
python manage.py migrate
```

5. Crear un superusuario:
```bash
python manage.py createsuperuser
```

6. Iniciar el servidor:
```bash
python manage.py runserver
```

## Uso

1. Acceder al panel de administración en `/admin/`
2. Agregar productos desde el panel de administración
3. Los usuarios pueden registrarse y comenzar a comprar

## Estructura del Proyecto

- `tienda/`: Aplicación principal
  - `models.py`: Modelos de datos
  - `views.py`: Vistas de la aplicación
  - `urls.py`: URLs de la aplicación
  - `forms.py`: Formularios
  - `templates/`: Plantillas HTML

## Próximos Pasos

- Implementar la integración con Transbank WebPay Plus
- Agregar sistema de categorías de productos
- Implementar búsqueda de productos
- Agregar sistema de reseñas
- Implementar sistema de cupones de descuento 