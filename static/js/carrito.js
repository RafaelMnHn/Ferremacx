let botones = document.getElementsByClassName('update-cart');

for (let i = 0; i < botones.length; i++) {
  botones[i].addEventListener('click', function () {
    let productId = this.dataset.product;
    let action = this.dataset.action;

    console.log('Product ID:', productId, 'Action:', action);

    fetch('/actualizar-item/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify({ productId: productId, action: action })
    })
    .then(res => res.json())
    .then(data => {
      console.log('Respuesta:', data);
      location.reload();  // Refresca la página para ver el carrito actualizado
    });
  });
}

// Función para obtener el token CSRF
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    let cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      let cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
