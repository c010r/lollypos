# Lollypos - Gastronomic Point of Sale System

Lollypos is a full-stack Point of Sale (POS) application designed for gastronomic establishments. It features a user-friendly frontend built with Next.js and a robust backend API powered by Django.

## Project Overview

*   **Frontend (`lollypos_frontend/`):** A Next.js application that provides the user interface for browsing the menu, creating, and managing orders.
*   **Backend (`lollypos_backend/`):** A Django application that serves a RESTful API for managing menu items and processing orders.

## Running the Application

To run the Lollypos system, both the backend and frontend applications must be running concurrently.

1.  **Start the Django Backend:**
    *   Navigate to the `lollypos_backend/` directory.
    *   Follow the setup and execution instructions in `lollypos_backend/README.md` to start the Django development server.
    *   Typically, this involves setting up a virtual environment, installing dependencies, running migrations, and then starting the server using `python manage.py runserver`.
    *   The backend API will usually be available at `http://localhost:8000`.

2.  **Start the Next.js Frontend:**
    *   Navigate to the `lollypos_frontend/` directory.
    *   Follow the setup and execution instructions in `lollypos_frontend/README.md` to start the Next.js development server.
    *   Typically, this involves installing dependencies and then starting the server using `npm run dev` or `yarn dev`.
    *   The frontend application will usually be available at `http://localhost:3000`.

Once both servers are running, you can access the Lollypos application by opening `http://localhost:3000` in your web browser.

## Further Information

*   For detailed backend setup and API documentation, see `lollypos_backend/README.md`.
*   For detailed frontend setup and component structure, see `lollypos_frontend/README.md`.
