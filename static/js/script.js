document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded and parsed');

    // Обработчик для кнопки "Скрыть все объекты"
    const toggleObjectsButton = document.getElementById('toggleObjects');
    console.log('Toggle button:', toggleObjectsButton);

    const backgroundContainer = document.getElementById('background-container');
    const backgroundArrows = document.querySelectorAll('.background-arrow');
    const chatbot = document.querySelector('.chatbot');
    
    console.log('Background container:', backgroundContainer);
    console.log('Background arrows:', backgroundArrows);
    console.log('Chatbot:', chatbot);

    let objectsHidden = false;

    if (toggleObjectsButton) {
        toggleObjectsButton.addEventListener('click', function(e) {
            e.preventDefault();
            objectsHidden = !objectsHidden;
            
            // Получаем все элементы, которые нужно скрывать
            const nav = document.querySelector('nav');
            const main = document.querySelector('main');
            const chatbot = document.querySelector('.chatbot');
            const footerContent = document.querySelector('.footer-content');
            const backgroundArrows = document.querySelectorAll('.background-arrow');

            // Скрываем/показываем основные элементы
            [nav, main, chatbot].forEach(element => {
                if (element) {
                    element.style.display = objectsHidden ? 'none' : '';
                }
            });

            // Обработка элементов в footer-content
            if (footerContent) {
                const footerItems = footerContent.querySelectorAll('.footer-item');
                footerItems.forEach(item => {
                    if (!item.contains(toggleObjectsButton)) {
                        item.style.visibility = objectsHidden ? 'hidden' : 'visible';
                    }
                });
            }

            // Скрываем/показываем стрелки фона
            backgroundArrows.forEach(arrow => {
                arrow.style.display = objectsHidden ? 'none' : 'block';
            });

            // Меняем текст кнопки
            this.textContent = objectsHidden ? 'Показать все объекты' : 'Скрыть все объекты';
        });
    } else {
        console.log('Toggle button not found');
    }
});
