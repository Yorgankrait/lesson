document.addEventListener('DOMContentLoaded', function() {
    // Создаем кнопку для чата, если её еще нет
    if (!document.querySelector('.chat-toggle')) {
        const chatToggle = document.createElement('button');
        chatToggle.className = 'chat-toggle';
        chatToggle.innerHTML = '<i class="fas fa-comments"></i>';
        document.body.appendChild(chatToggle);
    }

    const chatToggle = document.querySelector('.chat-toggle');
    const chatbot = document.querySelector('.chatbot');

    if (chatToggle && chatbot) {
        // Обработчик для открытия/закрытия чата
        chatToggle.addEventListener('click', function() {
            this.classList.toggle('active');
            if (this.classList.contains('active')) {
                chatbot.style.display = 'flex';
                // Прокручиваем чат к последнему сообщению
                const messages = document.getElementById('chatbotMessages');
                if (messages) {
                    messages.scrollTop = messages.scrollHeight;
                }
            } else {
                chatbot.style.display = 'none';
            }
        });

        // Закрытие чата при клике вне его области
        document.addEventListener('click', function(e) {
            if (!chatbot.contains(e.target) && !chatToggle.contains(e.target)) {
                chatToggle.classList.remove('active');
                chatbot.style.display = 'none';
            }
        });

        // Обработка изменения ориентации устройства
        window.addEventListener('orientationchange', function() {
            if (chatToggle.classList.contains('active')) {
                setTimeout(() => {
                    chatbot.style.height = '50vh';
                }, 100);
            }
        });
    }

    // Адаптация навигации для мобильных устройств
    const hamburgerMenu = document.querySelector('.hamburger-menu');
    const nav = document.querySelector('nav');

    if (hamburgerMenu && nav) {
        hamburgerMenu.addEventListener('click', function(e) {
            e.stopPropagation();
            nav.classList.toggle('mobile-active');
        });

        // Закрытие меню при клике вне его
        document.addEventListener('click', function(e) {
            if (!nav.contains(e.target) && !hamburgerMenu.contains(e.target)) {
                nav.classList.remove('mobile-active');
            }
        });
    }

    // Обработка скролла на мобильных устройствах
    let touchStartY = 0;
    document.addEventListener('touchstart', function(e) {
        touchStartY = e.touches[0].clientY;
    }, { passive: true });

    document.addEventListener('touchmove', function(e) {
        if (chatbot.style.display === 'flex') {
            const touchY = e.touches[0].clientY;
            const scrollingElement = document.getElementById('chatbotMessages');
            
            if (scrollingElement) {
                const isAtTop = scrollingElement.scrollTop === 0;
                const isAtBottom = scrollingElement.scrollHeight - scrollingElement.scrollTop === scrollingElement.clientHeight;
                
                if ((isAtTop && touchY > touchStartY) || (isAtBottom && touchY < touchStartY)) {
                    e.preventDefault();
                }
            }
        }
    }, { passive: false });
}); 