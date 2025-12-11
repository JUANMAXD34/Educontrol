function toggleFiltrosGenerales() {
  const lista = document.getElementById("listaFiltros");
  lista.style.display = (lista.style.display === "none" || lista.style.display === "") ? "block" : "none";
}

function aplicarFiltrosGenerales() {
  const filtroSeleccionado = parseInt(document.querySelector('input[name="filtro"]:checked').value);
  const texto = document.getElementById("buscador").value.toLowerCase();
  const desde = new Date(document.getElementById('desde').value);
  const hasta = new Date(document.getElementById('hasta').value);
  const filas = document.querySelectorAll(".tabla tbody tr");

  filas.forEach(fila => {
    let mostrar = true;

    if (texto) {
      const celda = fila.children[filtroSeleccionado].textContent.toLowerCase();
      if (!celda.includes(texto)) mostrar = false;
    }

    if (!isNaN(desde.getTime()) || !isNaN(hasta.getTime())) {
      const fechaTexto = fila.children[4].textContent.trim();
      const fechaPago = new Date(fechaTexto);
      if (!isNaN(desde.getTime()) && fechaPago < desde) mostrar = false;
      if (!isNaN(hasta.getTime()) && fechaPago > hasta) mostrar = false;
    }

    fila.style.display = mostrar ? "" : "none";
  });
}

document.querySelectorAll('input[name="filtro"]').forEach(radio => {
  radio.addEventListener('change', () => {
    const buscador = document.getElementById("buscador");
    buscador.value = "";
    buscador.placeholder = "Buscar por " + radio.parentElement.textContent.trim() + "...";
    aplicarFiltrosGenerales();
  });
});

function resetFiltrosGenerales() {
  const radios = document.querySelectorAll('input[name="filtro"]');
  const defaultRadio = radios[0];
  defaultRadio.checked = true;

  const buscador = document.getElementById("buscador");
  buscador.value = "";
  buscador.placeholder = "Buscar por " + defaultRadio.parentElement.textContent.trim() + "...";

  document.getElementById("desde").value = "";
  document.getElementById("hasta").value = "";

  document.querySelectorAll(".tabla tbody tr").forEach(fila => {
    fila.style.display = "";
  });

  document.getElementById("listaFiltros").style.display = "none";
}


document.addEventListener("DOMContentLoaded", () => {
  const modal = document.getElementById("igiak_modalAlumno");
  const btnBuscar = document.getElementById("igiak_btnBuscarAlumno");
  const buscador = document.getElementById("igiak_buscador");
  const btnToggleFiltros = document.getElementById("igiak_btnToggleFiltros");
  const btnResetFiltros = document.getElementById("igiak_btnResetFiltros");

  btnBuscar.addEventListener("click", () => {
    modal.showModal();
  });

  buscador.addEventListener("keyup", aplicarFiltrosAlumnos);

  btnToggleFiltros.addEventListener("click", () => {
    const lista = document.getElementById("igiak_listaFiltros");
    lista.style.display = lista.style.display === "none" ? "flex" : "none";
  });

  btnResetFiltros.addEventListener("click", resetFiltrosAlumnos);

  document.querySelectorAll("#igiak_tbodyAlumnos tr").forEach(fila => {
    fila.addEventListener("click", () => {
      const alumnoId = fila.dataset.id;
      const alumnoNombre = fila.dataset.nombre;
      document.getElementById("igiak_alumno_id").value = alumnoId;
      document.getElementById("igiak_alumno_nombre").value = alumnoNombre;
      modal.close();
    });
  });
});

function aplicarFiltrosAlumnos() {
  const filtro = document.querySelector("input[name='igiak_filtro']:checked").value;
  const texto = document.getElementById("igiak_buscador").value.toLowerCase();

  document.querySelectorAll("#igiak_tbodyAlumnos tr").forEach(fila => {
    let valor = "";
    if (filtro === "0") valor = fila.dataset.id;
    if (filtro === "1") valor = fila.dataset.nombre.toLowerCase();
    if (filtro === "2") valor = fila.dataset.grupo.toLowerCase();
    fila.style.display = valor.includes(texto) ? "" : "none";
  });
}

function resetFiltrosAlumnos() {
  const radios = document.querySelectorAll('input[name="igiak_filtro"]');
  const defaultRadio = radios[0];
  defaultRadio.checked = true;

  const buscador = document.getElementById("igiak_buscador");
  buscador.value = "";
  buscador.placeholder = "Buscar por " + defaultRadio.parentElement.textContent.trim() + "...";

  document.querySelectorAll("#igiak_tbodyAlumnos tr").forEach(fila => {
    fila.style.display = "";
  });
}
