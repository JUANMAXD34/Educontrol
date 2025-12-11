const modal = document.getElementById('modal');
const boton = document.getElementById('btn');
const cerrar = document.getElementById('btn-close');

boton.addEventListener('click', () => {
  modal.classList.remove('animate-out');
  modal.classList.add('animate-in');
  modal.showModal();
});

cerrar.addEventListener('click', () => {
  modal.classList.remove('animate-in');
  modal.classList.add('animate-out');
  setTimeout(() => {
    modal.close();
  }, 400);
});


function cerrarAlerta(id) {
  const alerta = document.getElementById(id);
  if (alerta) {
    alerta.style.opacity = '0';
    setTimeout(() => alerta.remove(), 500);
  }
}

window.addEventListener('DOMContentLoaded', () => {
  setTimeout(() => cerrarAlerta('alerta-error'), 4000);
  setTimeout(() => cerrarAlerta('alerta-ok'), 4000);
});


