console.log('auto_login.js loaded');

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded');
    const form = document.getElementById('login-form');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const loginButton = document.querySelector('.login-button');

    if (!form || !usernameInput || !passwordInput || !loginButton) {
        console.error('Required elements not found');
        return;
    }

    console.log('Form and inputs found');

    function attemptLogin() {
        console.log('Attempting login');
        if (usernameInput.value && passwordInput.value) {
            console.log('Username and password filled');
            const formData = new FormData(form);
            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            })
            .then(response => {
                console.log('Response status:', response.status);
                return response.json();
            })
            .then(data => {
                console.log('Response data:', data);
                if (data.success) {
                    console.log('Login successful, redirecting');
                    window.location.href = data.redirect_url;
                } else {
                    console.log('Login failed');
                    // Не очищаем поля ввода при неудачном входе
                }
            })
            .catch(error => console.error('Error:', error));
        } else {
            console.log('Username or password empty');
        }
    }

    let typingTimer;
    const doneTypingInterval = 1000; // 1 секунда

    function doneTyping() {
        if (usernameInput.value && passwordInput.value) {
            attemptLogin();
        }
    }

    usernameInput.addEventListener('input', () => {
        clearTimeout(typingTimer);
        typingTimer = setTimeout(doneTyping, doneTypingInterval);
    });

    passwordInput.addEventListener('input', () => {
        clearTimeout(typingTimer);
        typingTimer = setTimeout(doneTyping, doneTypingInterval);
    });

    // Обработчик события 'submit' для формы
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        attemptLogin();
    });

    // Показываем кнопку входа
    loginButton.style.display = 'block';

    console.log('Event listeners added');
});
