function buscadorGrupo() {
    const grupo = document.getElementById('Grupo').value.toLowerCase();
    const turno = document.getElementById('Turno').value.toLowerCase();
    const filas = document.querySelectorAll("#tablaGrupos tr");
    const tabla = document.getElementById("tablaGrupos");
    let contador = 1;
    let hayCoincidencias = false;

    for (let i = 1; i < filas.length; i++) {
        const celdaGrupo = filas[i].cells[2];
        const celdaTurno = filas[i].cells[3];

        if (celdaGrupo && celdaTurno) {
            const textoGrupo = celdaGrupo.textContent.toLowerCase();
            const textoTurno = celdaTurno.textContent.toLowerCase();
            const coincideGrupo = textoGrupo.startsWith(grupo);
            const coincideTurno = textoTurno.startsWith(turno);

            if (coincideGrupo && coincideTurno) {
                filas[i].style.display = "";
                filas[i].cells[0].textContent = contador;
                contador++;
                hayCoincidencias = true;
            } else {
                filas[i].style.display = "none";
            }
        }
    }

    tabla.style.display = hayCoincidencias ? "table" : "none";
}



document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("boton").addEventListener("click", buscadorGrupo);
});