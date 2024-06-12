document.addEventListener('DOMContentLoaded', () => {
    const searchForm = document.getElementById('search-form');
    const searchResults = document.getElementById('search-results');
    const addAllergenForm = document.getElementById('add-allergen-form');
    const allergenMessage = document.getElementById('add-allergen-message');
    const cart = document.getElementById('cart');

    searchForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const searchTerm = document.getElementById('search-term').value.toLowerCase();
        fetch(`/search_flavors?search_term=${searchTerm}`)
            .then(response => response.json())
            .then(data => {
                searchResults.innerHTML = '';
                if (data.length > 0) {
                    data.forEach(flavor => {
                        const li = document.createElement('li');
                        li.textContent = `${flavor[1]}: ${flavor[2]}`;
                        const addButton = document.createElement('button');
                        addButton.textContent = 'Add to Cart';
                        addButton.addEventListener('click', () => {
                            addToCart(flavor);
                        });
                        li.appendChild(addButton);
                        searchResults.appendChild(li);
                    });
                } else {
                    searchResults.innerHTML = '<li>No flavors found.</li>';
                }
            });
    });

    addAllergenForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const allergen = document.getElementById('allergen').value.toLowerCase();
        fetch('/add_allergen', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ allergen: allergen })
        })
        .then(response => response.json())
        .then(data => {
            allergenMessage.textContent = data.message;
        });
    });

    function addToCart(flavor) {
        const cartItems = JSON.parse(localStorage.getItem('cartItems')) || [];
        cartItems.push(flavor);
        localStorage.setItem('cartItems', JSON.stringify(cartItems));
        updateCart();
    }

    function updateCart() {
        const cartItems = JSON.parse(localStorage.getItem('cartItems')) || [];
        cart.innerHTML = '';
        cartItems.forEach((item, index) => {
            const li = document.createElement('li');
            li.textContent = `${item[1]}: ${item[2]}`;
            const removeButton = document.createElement('button');
            removeButton.textContent = 'Remove';
            removeButton.addEventListener('click', () => {
                removeFromCart(index);
            });
            li.appendChild(removeButton);
            cart.appendChild(li);
        });
    }

    function removeFromCart(index) {
        const cartItems = JSON.parse(localStorage.getItem('cartItems')) || [];
        cartItems.splice(index, 1);
        localStorage.setItem('cartItems', JSON.stringify(cartItems));
        updateCart();
    }

    updateCart();
});
