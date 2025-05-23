// static/main/cart.js

document.addEventListener('DOMContentLoaded', () => {
  const cartButtons = document.querySelectorAll('.add-to-cart');

  cartButtons.forEach(button => {
    button.addEventListener('click', (e) => {
      // Только если это кнопка "в корзину", а не "в избранное"
      if (!button.dataset.id) return;

      e.preventDefault();

      const id = button.dataset.id;
      const name = button.dataset.name;
      const price = button.dataset.price;

      const item = { id, name, price };

      let cart = JSON.parse(localStorage.getItem('cart')) || [];

      const exists = cart.find(i => i.id === id);
      if (!exists) {
        cart.push(item);
        localStorage.setItem('cart', JSON.stringify(cart));
        alert(`«${name}» добавлен в корзину!`);
      } else {
        alert(`«${name}» уже в корзине.`);
      }
    });
  });
});
