import MenuItemCard from './MenuItemCard';

export default function MenuList({ menuItems, addToCart }) {
    if (!menuItems || menuItems.length === 0) {
        return <p>No menu items available.</p>;
    }

    return (
        <div>
            {menuItems.map(item => (
                <MenuItemCard key={item.id} item={item} addToCart={addToCart} />
            ))}
        </div>
    );
}
