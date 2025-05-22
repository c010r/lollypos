# Lollypos Backend

This Django project serves as the backend API for the Lollypos system. It manages menu items, orders, and provides a RESTful API for the frontend.

## Project Setup

1.  **Create and Activate a Python Virtual Environment:**
    It's highly recommended to use a virtual environment to manage project dependencies.
    ```bash
    python -m venv venv
    # On Windows
    source venv\\Scripts\\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

2.  **Install Dependencies:**
    Navigate to the `lollypos_backend` directory (where this README is located) and install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run Database Migrations:**
    Apply the database schema changes:
    ```bash
    python manage.py migrate
    ```

4.  **Run the Development Server:**
    Start the Django development server:
    ```bash
    python manage.py runserver
    ```
    By default, the server will run on `http://localhost:8000`.

5.  **(Optional) Create a Superuser:**
    To access the Django admin interface, create a superuser:
    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts to set a username, email (optional), and password. You can then access the admin panel at `http://localhost:8000/admin/`.

## Core App (`pos_core`)

The `pos_core` app is the heart of the backend. It is responsible for:
*   Managing `MenuItem` data (name, description, price, category).
*   Handling `Order` creation and processing, including `OrderItem` details (which menu item, quantity, price at the time of order).

## API Endpoints

All API endpoints are prefixed with `/api/`.

### Menu Items

*   **Endpoint:** `GET /api/menu-items/`
    *   **Purpose:** Retrieve a list of all available menu items.
    *   **Success Response (200 OK):** An array of menu item objects.
        ```json
        [
            {
                "id": 1,
                "name": "Espresso",
                "description": "Strong black coffee",
                "price": "2.50",
                "category": "Drinks"
            },
            {
                "id": 2,
                "name": "Croissant",
                "description": "Buttery flaky pastry",
                "price": "3.00",
                "category": "Pastries"
            }
            // ... more items
        ]
        ```

### Orders

*   **Endpoint:** `POST /api/orders/`
    *   **Purpose:** Create a new order.
    *   **Request Body Format:** A JSON object containing a list of items.
        ```json
        {
            "items": [
                {
                    "menu_item": 1,  // ID of the MenuItem
                    "quantity": 2
                },
                {
                    "menu_item": 2,
                    "quantity": 1
                }
            ]
        }
        ```
    *   **Success Response (201 Created):** The created order object, including its items and current status.
        ```json
        {
            "id": 101,
            "items": [
                {
                    "menu_item": 1,
                    "quantity": 2
                },
                {
                    "menu_item": 2,
                    "quantity": 1
                }
            ],
            "status": "pending", // Default status upon creation
            "timestamp": "2023-10-27T10:30:00Z"
        }
        ```
    *   **Error Responses (e.g., 400 Bad Request):**
        *   If `items` is missing or empty.
        *   If a `menu_item` ID is invalid or does not exist.
        *   If `quantity` is missing, not a positive integer.
        *   Example error for invalid menu item ID:
            ```json
            {
                "items": [
                    {
                        "menu_item": ["Invalid pk \"999\" - object does not exist."]
                    }
                ]
            }
            ```
