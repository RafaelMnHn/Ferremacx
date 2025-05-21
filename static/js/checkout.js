console.log('el penoso');
document.getElementById('form-envio').addEventListener('submit', function (e) {
    e.preventDefault();

    const direccion = this.direccion.value.trim();
    const region = this.region.value.trim();
    const comuna = this.comuna.value.trim();
    const ciudad = this.ciudad.value.trim();

    if (!direccion || !region || !comuna || !ciudad) {
        alert('Por favor completa todos los campos de envío.');
        return;
    }

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
        if (data.mensaje) {
            alert(data.mensaje);
            window.location.href = "{% url 'tienda' %}";  
        }   else if (data.error) {
            alert('Error: ' + data.error);
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