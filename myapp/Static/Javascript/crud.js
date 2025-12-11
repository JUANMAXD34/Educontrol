function manejarModal(selectorAbrir, selectorCerrar, prefix) {
    document.querySelectorAll(selectorAbrir).forEach(btn => {
        btn.addEventListener('click', () => {
            const id = btn.dataset.id;
            const modal = document.getElementById(`${prefix}-${id}`);
            modal.classList.remove('animate-out');
            modal.classList.add('animate-in');
            modal.showModal();
        });
    });

    document.querySelectorAll(selectorCerrar).forEach(btn => {
        btn.addEventListener('click', () => {
            const id = btn.dataset.id;
            const modal = document.getElementById(`${prefix}-${id}`);
            modal.classList.remove('animate-in');
            modal.classList.add('animate-out');
            setTimeout(() => modal.close(), 300);
        });
    });
}

manejarModal('.abrir-modal', '.cerrar-modal', 'modal');
manejarModal('.abrir-actualizar', '.cerrar-actualizar', 'ventana-modal');

function cerrarAlerta(id) {
    const alerta = document.getElementById(id);
    if (alerta) {
        alerta.style.opacity = '0';
        setTimeout(() => alerta.remove(), 700);
    }
}

window.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => cerrarAlerta('alerta-error'), 4000);
    setTimeout(() => cerrarAlerta('alerta-ok'), 4000);
});