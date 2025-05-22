# Lollypos Frontend

This Next.js application serves as the user interface for the Lollypos system. It allows users to browse the menu, select items, and place orders by interacting with the Lollypos backend API.

## Project Setup

1.  **Prerequisites:**
    *   Ensure you have [Node.js](https://nodejs.org/) installed (which includes npm). If you prefer Yarn, ensure it's installed.

2.  **Install Dependencies:**
    Navigate to the `lollypos_frontend` directory (where this README is located) and install the required packages:
    ```bash
    npm install
    ```
    Alternatively, if you are using Yarn:
    ```bash
    yarn install
    ```

3.  **Run the Development Server:**
    Start the Next.js development server:
    ```bash
    npm run dev
    ```
    Alternatively, if you are using Yarn:
    ```bash
    yarn dev
    ```
    By default, the server will run on `http://localhost:3000`.

## Project Structure

The project follows a standard Next.js (with App Router) structure:

*   **`app/`**: Contains all the pages and routes for the application.
    *   **`app/menu/page.js`**: The main page for displaying the menu and allowing users to create an order.
*   **`components/`**: Houses reusable React components used across different pages.
    *   **`components/MenuItemCard.js`**: A card component to display details of a single menu item and provide a button to add it to the current order.
    *   **`components/MenuList.js`**: A component that takes a list of menu items and renders a `MenuItemCard` for each.
    *   **`components/OrderCart.js`**: A component that displays the items currently added to the order. It allows users to adjust quantities, remove items, and finally place the order.
*   **`services/`**: Contains modules responsible for interacting with external APIs, primarily the Lollypos backend.
    *   **`services/api.js`**: Includes functions like `fetchMenuItems()` to get menu data and `createOrder()` to submit new orders to the backend.

## Backend Connection

The frontend application expects the Lollypos Django backend API to be running and accessible at:
**`http://localhost:8000`**

Ensure the backend server is started and running before attempting to use the frontend to browse items or place orders. If the backend is not available, API calls will fail, and the application will not function correctly.
