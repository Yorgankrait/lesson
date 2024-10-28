function toggleMenu() {
    const menuContent = document.getElementById('menuContent');
    menuContent.classList.toggle('show');
    
    // Закрываем меню при клике вне его
    document.addEventListener('click', function closeMenu(e) {
        if (!e.target.closest('.hamburger-menu')) {
            menuContent.classList.remove('show');
            document.removeEventListener('click', closeMenu);
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const mainMenuButton = document.getElementById('mainMenuButton');
    const secondaryMenuButton = document.getElementById('secondaryMenuButton');
    const nav = document.querySelector('nav');

    // Обработчик для основного меню
    mainMenuButton.addEventListener('click', function(e) {
        e.stopPropagation();
        nav.classList.toggle('active');
    });

    // Обработчик для второго меню
    secondaryMenuButton.addEventListener('click', function(e) {
        e.stopPropagation();
        console.log('Второе меню');
        // Здесь можно добавить логику для второго меню
    });

    // Закрытие меню при клике вне его (только на мобильных)
    if (window.innerWidth <= 768) {
        document.addEventListener('click', function(event) {
            if (!event.target.closest('nav') && 
                !event.target.closest('#mainMenuButton')) {
                nav.classList.remove('active');
            }
        });
    }
});
