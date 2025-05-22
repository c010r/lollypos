export default function OrderCart({ cartItems, removeFromCart, updateQuantity, submitOrder }) {
    if (!cartItems || cartItems.length === 0) {
        return (
            <div style={{ marginTop: '20px', padding: '10px', border: '1px solid #ddd' }}>
                <h2>Current Order</h2>
                <p>Your cart is empty.</p>
            </div>
        );
    }

    const calculateGrandTotal = () => {
        return cartItems.reduce((total, item) => total + (Number(item.price) * item.quantity), 0).toFixed(2);
    };

    return (
        <div style={{ marginTop: '20px', padding: '10px', border: '1px solid #007bff', borderRadius: '5px' }}>
            <h2>Current Order</h2>
            {cartItems.map(item => (
                <div key={item.id} style={{ marginBottom: '10px', padding: '10px', borderBottom: '1px solid #eee' }}>
                    <h4>{item.name}</h4>
                    <p>Price: ${Number(item.price).toFixed(2)}</p>
                    <p>Quantity: {item.quantity}</p>
                    <p>Total: ${(Number(item.price) * item.quantity).toFixed(2)}</p>
                    <div>
                        <button onClick={() => updateQuantity(item.id, item.quantity + 1)} style={{ marginRight: '5px' }}>+</button>
                        <button onClick={() => updateQuantity(item.id, item.quantity - 1)} style={{ marginRight: '5px' }}>-</button>
                        <button onClick={() => removeFromCart(item.id)}>Remove</button>
                    </div>
                </div>
            ))}
            <h3>Grand Total: ${calculateGrandTotal()}</h3>
            <button 
                onClick={submitOrder} 
                style={{ 
                    marginTop: '15px', 
                    padding: '10px 15px', 
                    backgroundColor: '#28a745', 
                    color: 'white', 
                    border: 'none', 
                    borderRadius: '5px',
                    cursor: 'pointer'
                }}
            >
                Place Order
            </button>
        </div>
    );
}
