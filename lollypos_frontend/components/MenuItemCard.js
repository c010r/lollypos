export default function MenuItemCard({ item, addToCart }) {
    if (!item) {
        return null;
    }

    const handleAddToCart = () => {
        if (addToCart) {
            addToCart(item);
        }
    };

    return (
        <div style={{ border: '1px solid #ccc', margin: '10px', padding: '10px', borderRadius: '5px' }}>
            <h3>{item.name}</h3>
            <p>{item.description || 'No description available.'}</p>
            <p>Price: ${Number(item.price).toFixed(2)}</p>
            {item.category && <p><em>Category: {item.category}</em></p>}
            <button onClick={handleAddToCart} style={{ marginTop: '10px', padding: '5px 10px' }}>
                Add to Order
            </button>
        </div>
    );
}
