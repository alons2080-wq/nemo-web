// Crear el elemento del cursor dinámicamente
const cursor = document.createElement('div');
cursor.id = 'custom-cursor';
document.body.appendChild(cursor);

document.addEventListener('mousemove', (e) => {
    // Sincroniza la posición del div con el mouse real
    cursor.style.left = `${e.clientX}px`;
    cursor.style.top = `${e.clientY}px`;
});

// Detectar cuando el mouse está sobre algo interactivo
const links = document.querySelectorAll('a, button, .social-link, iframe');

links.forEach(link => {
    link.addEventListener('mouseenter', () => {
        cursor.classList.add('link-hover');
    });
    link.addEventListener('mouseleave', () => {
        cursor.classList.remove('link-hover');
    });
});
