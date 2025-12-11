function toggleFiltros() {
    const lista = document.getElementById("listaFiltros");
    lista.style.display = lista.style.display === "inline-grid" ? "none" : "inline-grid";
}

function filtrarTabla() {
    const input = document.getElementById("buscador").value.toLowerCase();
    const filtroSeleccionado = document.querySelector(".lista-filtros input[type='radio']:checked");
    const tabla = document.getElementById("tabla");
    const filas = tabla.getElementsByTagName("tbody")[0].getElementsByTagName("tr");

    for (let fila of filas) {
        const celda = fila.getElementsByTagName("td")[filtroSeleccionado.value];
        fila.style.display = celda && celda.textContent.toLowerCase().includes(input) ? "" : "none";
    }
}

document.querySelectorAll(".lista-filtros input[type='radio']").forEach((radio) => {
    radio.addEventListener("change", () => {
        const buscador = document.getElementById("buscador");
        const nombres = ["ID...", "Nombre completo...", "Edad...", "Teléfono...", "Correo electrónico..."];
        buscador.placeholder = `Buscar por ${nombres[radio.value]}`;
        buscador.value = "";
        filtrarTabla();
    });
});
