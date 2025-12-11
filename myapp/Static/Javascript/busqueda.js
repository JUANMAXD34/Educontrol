document.addEventListener("DOMContentLoaded", function() {
    const filasPorPagina = 10;
    const tabla = document.querySelector(".tabla tbody");
    const filas = Array.from(tabla.querySelectorAll("tr"));
    const paginacion = document.createElement("div");
    paginacion.classList.add("pagination");
    tabla.parentElement.appendChild(paginacion);

    let paginaActual = 1;

    function mostrarPagina(pagina) {
        paginaActual = pagina;
        const inicio = (pagina - 1) * filasPorPagina;
        const fin = inicio + filasPorPagina;

        filas.forEach((fila, i) => {
            fila.style.display = (i >= inicio && i < fin) ? "" : "none";
        });

        renderBotones();
    }

    function renderBotones() {
        const totalPaginas = Math.ceil(filas.length / filasPorPagina);
        paginacion.innerHTML = "";

        for (let i = 1; i <= totalPaginas; i++) {
            const btn = document.createElement("button");
            btn.textContent = i;
            if (i === paginaActual) btn.classList.add("active");
            btn.addEventListener("click", () => mostrarPagina(i));
            paginacion.appendChild(btn);
        }
    }
    mostrarPagina(1);
});