# LollyPOS - Sistema de Punto de Venta

LollyPOS es un sistema moderno de punto de venta (POS) diseñado para restaurantes y tiendas minoristas.

## Estructura del proyecto

El proyecto está dividido en dos componentes principales:

### Backend (API REST con Django)

- Autenticación basada en JWT
- Gestión de empleados y roles
- Inventario y gestión de productos
- Procesamiento de pedidos y ventas
- Informes y análisis

### Frontend (Next.js + Material UI)

- Interfaz de usuario moderna y responsive
- Dashboard para análisis en tiempo real
- Gestión de mesas y pedidos
- Reportes e informes visuales
- Autenticación segura

## Requisitos

### Backend
- Python 3.8+
- Django 4.2+
- Django REST Framework

### Frontend
- Node.js 18+
- Next.js 14+
- Material UI 7+

## Configuración e instalación

### Backend

```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Pruebas

Para ejecutar las pruebas de autenticación:

```bash
python test_auth.py
```

## Licencia

Este proyecto está bajo licencia privada.
