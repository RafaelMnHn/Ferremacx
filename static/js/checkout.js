document.addEventListener('DOMContentLoaded', function () {  
  const form = document.getElementById('form-envio');
  if (!form) return;
  
  const ordenTotal = parseFloat(form.dataset.total);

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    const datos = {
      direccion: this.direccion.value,
      ciudad: this.ciudad.value,
      comuna: this.comuna.value,
      region: this.region.value,
      total: ordenTotal
    };

    fetch('/procesar-orden/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify(datos)
    })
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        alert('Error: ' + data.error);
      } else {
        window.location.href = "/iniciar-pago-rest/";
      }
    });
  });

    function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }
});