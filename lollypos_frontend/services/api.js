export async function fetchMenuItems() {
    try {
        const response = await fetch('http://localhost:8000/api/menu-items/');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Failed to fetch menu items:", error);
        throw error; // Re-throw the error to be handled by the caller
    }
}

export async function createOrder(orderData) {
    try {
        const response = await fetch('http://localhost:8000/api/orders/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(orderData),
        });
        if (!response.ok) {
            // Try to parse the error response from the server
            const errorBody = await response.json().catch(() => ({ detail: `HTTP error! status: ${response.status}` }));
            throw new Error(errorBody.detail || `HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Failed to create order:", error);
        throw error; // Re-throw the error to be handled by the caller
    }
}
