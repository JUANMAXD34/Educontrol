document.addEventListener('DOMContentLoaded', () => {
    const fotoInput = document.getElementById('{{ form.foto.auto_id }}');
    const nombreSpan = document.getElementById('foto-nombre');
    fotoInput.addEventListener('change', function () {
        const archivo = this.files[0];
        const nombre = archivo?.name || 'Selecciona una imagen';
        nombreSpan.textContent = nombre;
    });
    const formularios = document.querySelectorAll('.formularios');
    formularios.forEach((formulario, index) => {
        const input = formulario.querySelector('input[type="file"]');
        const nombreSpan = formulario.querySelector(`#foto-nombre-${index + 1}`);
        if (input && nombreSpan) {
            input.addEventListener('change', function () {
                const archivo = this.files[0];
                const nombre = archivo?.name || 'Selecciona una imagen';
                nombreSpan.textContent = nombre;
            });
        }
    });
});
document.addEventListener('DOMContentLoaded', () => {
    const fileUploads = document.querySelectorAll('.file-upload');
    fileUploads.forEach(upload => {
        const input = upload.querySelector('input[type="file"]');
        const nombreSpan = upload.querySelector('span[id$="-nombre"]');
        if (input && nombreSpan) {
            input.addEventListener('change', function () {
                const archivo = this.files[0];
                const nombre = archivo?.name||'Selecciona un archivo';
                nombreSpan.textContent = nombre;
            });
        }
    });
});
