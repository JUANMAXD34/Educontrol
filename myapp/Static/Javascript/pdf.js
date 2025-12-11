function descargarPDF() {
    const elemento = document.getElementById('tabla-alumnos');
    const opciones = {
        margin:       0,
        filename:     'alumnos.pdf',
        image:        { type: 'jpeg', quality: 0.98 },
        html2canvas:  { scale: 2 },
        jsPDF:        { unit: 'in', format: 'letter', orientation: 'portrait' }
    };
    html2pdf().set(opciones).from(elemento).save();
}

window.onload = function() {
    const elemento = document.getElementById('contenido-pdf');
    const opciones = {
        margin: 0,
        filename: `Profesor.pdf`,
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2 },
        jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
    };
    html2pdf().set(opciones).from(elemento).save()
};