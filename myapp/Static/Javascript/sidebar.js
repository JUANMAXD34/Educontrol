document.addEventListener('DOMContentLoaded', () => {
    const menu = document.getElementById('menu');
    const sidebar = document.getElementById('sidebar');
    const main = document.getElementById('contenido');
    const encabezado = document.getElementById('encabezado');
    const parte = document.getElementById('content');

    menu.addEventListener('click', () => {
        sidebar.classList.toggle('menu-toggle');
        menu.classList.toggle('menu-toggle');
        main.classList.toggle('menu-toggle');
        encabezado.classList.toggle('menu-toggle');
        parte.classList.toggle('menu-toggle');
    });
});