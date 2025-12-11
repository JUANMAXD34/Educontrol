document.addEventListener("DOMContentLoaded", function() {
    const nombreInput = document.querySelector("#id_nombre_tutor");
    const apellidosInput = document.querySelector("#id_apellidos_tutor");
    const Input = document.querySelector("#id_nombre_alumno");
    const apelliInput = document.querySelector("#id_apellidos_alumno");

    function soloLetras(e) {
        let char = String.fromCharCode(e.keyCode);
        let regex = /^[a-zA-ZÁÉÍÓÚáéíóúñÑ\s]+$/;
        if (!regex.test(char)) {
            e.preventDefault();
        }
    }

    nombreInput.addEventListener("keypress", soloLetras);
    apellidosInput.addEventListener("keypress", soloLetras);
    Input.addEventListener("keypress", soloLetras);
    apelliInput.addEventListener("keypress", soloLetras);

    const telefonoInput = document.querySelector("#id_telefono");

    function soloNumeros(e) {
        let char = String.fromCharCode(e.keyCode);
        let regex = /^[0-9]+$/;
        if (!regex.test(char)) {
            e.preventDefault();
        }
    }

    telefonoInput.addEventListener("keypress", soloNumeros);
});
document.getElementById("igiak_btnBuscarTutor").addEventListener("click", () => {
    document.getElementById("igiak_modalTutor").showModal();
});
document.querySelector("#igiak_modalTutor button[value='cancel']").addEventListener("click", () => {
    document.getElementById("igiak_modalTutor").close();
});

document.getElementById("igiak_btnBuscarGrupo").addEventListener("click", () => {
    document.getElementById("igiak_modalGrupo").showModal();
});
document.querySelector("#igiak_modalGrupo button[value='cancel']").addEventListener("click", () => {
    document.getElementById("igiak_modalGrupo").close();
});
document.querySelectorAll(".fila-grupo").forEach(fila => {
    fila.addEventListener("click", () => {
        document.getElementById("igiak_grupo_id").value = fila.dataset.id;
        document.getElementById("igiak_grupo_nombre").value = fila.dataset.nombre;
        document.getElementById("igiak_modalGrupo").close();
    });
});
document.getElementById("igiak_btnSeleccionarTutores").addEventListener("click", () => {
    const seleccionados = Array.from(document.querySelectorAll(".chk-tutor:checked"));

    if (seleccionados.length > 3) {
        alert("Solo puedes seleccionar máximo 3 tutores.");
        return;
    }

    const ids = seleccionados.map(chk => chk.dataset.id);
    const nombres = seleccionados.map(chk => chk.dataset.nombre);

    document.getElementById("igiak_tutor_ids").value = ids.join(",");
    document.getElementById("igiak_tutor_nombres").value = nombres.join(", ");

    document.getElementById("igiak_modalTutor").close();
});
document.getElementById("igiak_btnToggleFiltrosGrupo").addEventListener("click", () => {
    const lista = document.getElementById("igiak_listaFiltrosGrupo");
    lista.style.display = lista.style.display === "none" ? "block" : "none";
});

document.getElementById("igiak_btnResetFiltrosGrupo").addEventListener("click", () => {
    document.getElementById("igiak_buscadorGrupo").value = "";
    document.querySelector("input[name='igiak_filtroGrupo'][value='0']").checked = true;
    filtrarTablaGrupo();
});

document.getElementById("igiak_buscadorGrupo").addEventListener("input", filtrarTablaGrupo);

function filtrarTablaGrupo() {
    const filtro = document.querySelector("input[name='igiak_filtroGrupo']:checked").value;
    const texto = document.getElementById("igiak_buscadorGrupo").value.toLowerCase();
    document.querySelectorAll("#igiak_tbodyGrupos tr").forEach(tr => {
        let campo = "";
        if (filtro === "0") campo = tr.children[0].textContent.toLowerCase(); // ID
        if (filtro === "1") campo = tr.children[1].textContent.toLowerCase(); // Nombre
        tr.style.display = campo.includes(texto) ? "" : "none";
    });
}
document.getElementById("igiak_btnToggleFiltrosTutor").addEventListener("click", () => {
    const lista = document.getElementById("igiak_listaFiltrosTutor");
    lista.style.display = lista.style.display === "none" ? "block" : "none";
});

document.getElementById("igiak_btnResetFiltrosTutor").addEventListener("click", () => {
    document.getElementById("igiak_buscadorTutor").value = "";
    document.querySelector("input[name='igiak_filtroTutor'][value='0']").checked = true;
    filtrarTablaTutor();
});

document.getElementById("igiak_buscadorTutor").addEventListener("input", filtrarTablaTutor);

function filtrarTablaTutor() {
    const filtro = document.querySelector("input[name='igiak_filtroTutor']:checked").value;
    const texto = document.getElementById("igiak_buscadorTutor").value.toLowerCase();
    document.querySelectorAll("#igiak_tbodyTutores tr").forEach(tr => {
        let campo = "";
        if (filtro === "0") campo = tr.children[1].textContent.toLowerCase();
        if (filtro === "1") campo = tr.children[2].textContent.toLowerCase();
        if (filtro === "2") campo = tr.children[3].textContent.toLowerCase();
        if (filtro === "3") campo = tr.children[4].textContent.toLowerCase();
        tr.style.display = campo.includes(texto) ? "" : "none";
    });
}
