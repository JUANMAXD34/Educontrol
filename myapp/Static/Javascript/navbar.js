const navbar = document.querySelector('header');

document.addEventListener('scroll', () => {
    const scroll = window.scrollY;
    if (scroll > 400) {
        navbar.classList.add('visible');
    } else {
        navbar.classList.remove('visible');
    }
});

