document.addEventListener('DOMContentLoaded', function() {
    console.log('Страница загружена полностью!');
    alert('Страница загружена полностью!');
});

document.querySelectorAll('.nav-link').forEach(link => {
    if(link.href === window.location.href) {
        link.classList.add('active');
    }
});