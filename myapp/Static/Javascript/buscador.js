    function toggleFiltrosGenerales() {
    const lista = document.getElementById("listaFiltros");
    lista.style.display = (lista.style.display === "none" || lista.style.display === "") ? "block" : "none";
}

function resetFiltrosGenerales() {
    document.querySelector('input[name="filtro"][value="0"]').checked = true;
    const buscador = document.getElementById("buscador");
    buscador.value = "";
    buscador.placeholder = "Buscar por ID...";
    aplicarFiltrosGenerales();
}

function aplicarFiltrosGenerales() {
    const filtroSeleccionado = document.querySelector('input[name="filtro"]:checked').value;
    const buscador = document.getElementById("buscador");
    const texto = buscador.value.toLowerCase();

    // Cambiar placeholder dinámicamente
    switch (filtroSeleccionado) {
        case "0": buscador.placeholder = "Buscar por ID..."; break;
        case "1": buscador.placeholder = "Buscar por CURP..."; break;
        case "2": buscador.placeholder = "Buscar por Nombre Completo..."; break;
        case "3": buscador.placeholder = "Buscar por Grupo..."; break;
        case "4": buscador.placeholder = "Buscar por Tutores..."; break;
    }

    const filas = document.querySelectorAll("table tbody tr");
    filas.forEach(fila => {
        const celdas = fila.querySelectorAll("td");
        const valorCelda = celdas[parseInt(filtroSeleccionado)].textContent.toLowerCase();
        fila.style.display = valorCelda.includes(texto) ? "" : "none";
    });
}
document.querySelectorAll('input[name="filtro"]').forEach(radio => {
    radio.addEventListener('change', aplicarFiltrosGenerales);
});

const abrir_alumno = document.getElementById('abrir-alumno');
const abrir_tutor = document.getElementById('abrir-tutor');
const cerrar_alumno = document.getElementById('cerrar-alumno');
const cerrar_tutor = document.getElementById('cerrar-tutor');
const modal_alumno = document.getElementById('modal-alumno');
const modal_tutor = document.getElementById('modal-tutor');

abrir_alumno.addEventListener('click',()=>{
    modal_alumno.showModal();
});
cerrar_alumno.addEventListener('click',()=>{
    modal_alumno.close();
});
abrir_tutor.addEventListener('click',()=>{
    modal_tutor.showModal();
});
cerrar_tutor.addEventListener('click',()=>{
    modal_tutor.close();
});
