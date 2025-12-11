

function filtrarTabla() {
    const input = document.getElementById("buscador");
    const filtro = input.value.toLowerCase();
    const filas = document.querySelectorAll("table tr");

    for (let i = 1; i < filas.length; i++) {
        const celdaNombre = filas[i].cells[0];
        if (celdaNombre) {
            const texto = celdaNombre.textContent.toLowerCase();
            filas[i].style.display = texto.startsWith(filtro) ? "" : "none";
        }
    }
}

function seleccionar(checkbox){
    const checkboxs = document.getElementsByName('opcion');
    const marcado = checkbox.checked;
    Array.from(checkboxs).forEach((cb) => {
        if( cb !== checkbox) cb.checked = false
    });
}

const btn_cerrar = document.getElementById('btn-cerrar');
const modal = document.getElementById('modal')
const boton = document.getElementById('boton')

boton.addEventListener('click',()=>{
    modal.classList.remove('animate-out');
    modal.classList.add('animate-in');
    modal.showModal();
})
btn_cerrar.addEventListener('click', () => {
    modal.classList.remove('animate-in');
    modal.classList.add('animate-out');
    modal.addEventListener('animationend', () => {
        modal.close();
    }, { once: true });
});


document.addEventListener('DOMContentLoaded', () => {
    const uploads = document.querySelectorAll('.file-upload');

    uploads.forEach(upload => {
        const input = upload.querySelector('input[type="file"]');
        const span = upload.querySelector('span[id$="-nombre"]'); 
        if (input && span) {
            const defaultText = span.textContent; 
            input.addEventListener('change', function () {
                const archivo = this.files[0];
                span.textContent = archivo ? archivo.name : defaultText;
            });
        }
    });
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


