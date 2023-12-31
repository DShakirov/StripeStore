var stripe = Stripe('pk_test_51OSF29Aq9HZcM26tKtfxBbRcfqzEEzgFoDmPT7Ux1wn6IRgZT5IEezB3oRhpu1PVpdnBTJvOkjEat4R7R0oLGE5b00pACFP023');
// Fetch items from server
fetch('/api/items')
  .then(response => response.json())
  .then(data => {
    const itemsContainer = document.getElementById('items-container');
    data.forEach(item => {
      const itemElement = document.createElement('div');
      itemElement.innerHTML = `
        <h3>${item.name}</h3>
        <p>${item.description}</p>
        <p>Price: $${item.price}</p>
        <button onclick="addToCart(${item.id}, '${item.name}', '${item.price}')">Add to Cart</button>
      `;
      itemsContainer.appendChild(itemElement);
    });
  })
  .catch(error => console.error(error));

// Cart
let cart = [];

function addToCart(itemId, itemName, itemPrice) {
    cart.push({ id: itemId, name: itemName, price: itemPrice }); // Add item name to cart
    updateCart();
}

function updateCart() {
    const cartContainer = document.getElementById('cart-container');
    cartContainer.innerHTML = '';

    cart.forEach(item => {
        const cartItemElement = document.createElement('div');
        cartItemElement.innerHTML = `
            <p>Item Name: ${item.name}</p>
        `;
        cartContainer.appendChild(cartItemElement);
    });
}
// Checkout form submit event
const checkoutForm = document.getElementById('checkout-form');
checkoutForm.addEventListener('submit', (event) => {
    event.preventDefault();

    const cardNumber = document.querySelector('input[name="cardNumber"]').value;
    const cardExpiry = document.querySelector('input[name="cardExpiry"]').value;
    const cardCvc = document.querySelector('input[name="cardCvc"]').value;
    const data = {
        cart
    };
    // Send data to backend
    var csrftoken = getCookie('csrftoken'); // Получение CSRF-токена из куки
    fetch('/api/checkout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken // Установка CSRF-токена в заголовке запроса
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            // Handle success response from backend
            console.log(data);
            // Access the clientSecret from the backend response
            const clientSecret = data.clientSecret;
            stripe.confirmCardPayment(clientSecret, {
                payment_method: {
        card: {
            number: cardNumber,
            exp_month: cardExpiry.split('/')[0].trim(),
            exp_year: cardExpiry.split('/')[1].trim(),
            cvc: cardCvc
        },
                    billing_details: {
                        name: 'John Doe'
                    },
                }
            }).then(function(result) {
                if (result.error) {
                    // Ошибка обработки оплаты
                } else {
                    // Оплата прошла успешно
                }
            });
        })
        .catch(error => {
            // Handle error response from backend
            console.error(error);
        });
});

    // Функция для получения значения CSRF-токена из куки
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }