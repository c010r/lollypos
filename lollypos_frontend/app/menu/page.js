"use client";

import { useState, useEffect } from 'react';
import { fetchMenuItems, createOrder } from '../../services/api'; // Import createOrder
import MenuList from '../../components/MenuList';
import OrderCart from '../../components/OrderCart'; // Import OrderCart

export default function MenuPage() {
    const [menuItems, setMenuItems] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [cartItems, setCartItems] = useState([]);
    const [orderStatus, setOrderStatus] = useState(''); // For success/error messages

    const addToCart = (menuItem) => {
        setCartItems(prevItems => {
            const existingItem = prevItems.find(item => item.id === menuItem.id);
            if (existingItem) {
                return prevItems.map(item =>
                    item.id === menuItem.id ? { ...item, quantity: item.quantity + 1 } : item
                );
            }
            return [...prevItems, { ...menuItem, quantity: 1 }];
        });
    };

    const removeFromCart = (menuItemId) => {
        setCartItems(prevItems => prevItems.filter(item => item.id !== menuItemId));
    };

    const updateQuantity = (menuItemId, newQuantity) => {
        if (newQuantity < 1) {
            removeFromCart(menuItemId); // Or set to 1, depending on desired behavior
            return;
        }
        setCartItems(prevItems =>
            prevItems.map(item =>
                item.id === menuItemId ? { ...item, quantity: newQuantity } : item
            )
        );
    };

    useEffect(() => {
        async function loadMenuItems() {
            try {
                setLoading(true);
                const data = await fetchMenuItems();
                setMenuItems(data);
                setError(null);
            } catch (err) {
                setError(err.message || "Failed to load menu items.");
                setMenuItems([]); // Ensure menuItems is an empty array on error
            } finally {
                setLoading(false);
            }
        }
        loadMenuItems();
    }, []);

    if (loading) {
        return <p>Loading menu items...</p>;
    }

    if (error) {
        return <p>Error loading menu items: {error}</p>;
    }

    // submitOrder function
    const submitOrder = async () => {
        if (cartItems.length === 0) {
            setOrderStatus("Cannot place an empty order.");
            setTimeout(() => setOrderStatus(''), 3000); // Clear message after 3 seconds
            return;
        }

        const orderData = {
            items: cartItems.map(item => ({
                menu_item: item.id, // API expects 'menu_item' which is the ID
                quantity: item.quantity
            }))
        };

        try {
            setOrderStatus('Placing order...');
            const result = await createOrder(orderData);
            setOrderStatus(`Order placed successfully! Order ID: ${result.id}`);
            setCartItems([]); // Clear the cart
            setTimeout(() => setOrderStatus(''), 5000); // Clear message after 5 seconds
        } catch (err) {
            setOrderStatus(`Error placing order: ${err.message}`);
            setTimeout(() => setOrderStatus(''), 5000); // Clear message after 5 seconds
        }
    };

    if (loading) {
        return <p>Loading menu items...</p>;
    }

    if (error) {
        return <p>Error loading menu items: {error}</p>;
    }

    return (
        <div style={{ display: 'flex', flexDirection: 'row', gap: '20px', padding: '20px' }}>
            <div style={{ flex: 2 }}>
                <h1>Our Menu</h1>
                <MenuList menuItems={menuItems} addToCart={addToCart} />
            </div>
            <div style={{ flex: 1, position: 'sticky', top: '20px', alignSelf: 'flex-start' }}>
                <OrderCart 
                    cartItems={cartItems}
                    removeFromCart={removeFromCart}
                    updateQuantity={updateQuantity}
                    submitOrder={submitOrder}
                />
                {orderStatus && 
                    <p style={{ 
                        marginTop: '15px', 
                        padding: '10px',
                        borderRadius: '5px',
                        backgroundColor: orderStatus.includes('Error') || orderStatus.includes('Cannot') ? '#ffebee' : '#e8f5e9', // Softer red/green
                        color: orderStatus.includes('Error') || orderStatus.includes('Cannot') ? '#c62828' : '#2e7d32', // Darker text for contrast
                        border: `1px solid ${orderStatus.includes('Error') || orderStatus.includes('Cannot') ? '#ef9a9a' : '#a5d6a7'}`, // Lighter border
                        textAlign: 'center'
                    }}>
                        {orderStatus}
                    </p>
                }
            </div>
            {/* <div style={{ marginTop: '20px', border: '1px solid green', padding: '10px' }}>
                <h2>Current Cart</h2>
                {cartItems.length === 0 ? <p>Cart is empty</p> : 
                    cartItems.map(item => (
                        <div key={item.id}>
                            {item.name} - Qty: {item.quantity} 
                            <button onClick={() => updateQuantity(item.id, item.quantity + 1)}>+</button>
                            <button onClick={() => updateQuantity(item.id, item.quantity - 1)}>-</button>
                            <button onClick={() => removeFromCart(item.id)}>Remove</button>
                        </div>
                    ))
                }
            </div> */}
        </div>
    );
}
