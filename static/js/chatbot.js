document.addEventListener('DOMContentLoaded', function() {
    const chatbotMessages = document.getElementById('chatbotMessages');
    const chatbotInput = document.getElementById('chatbotInput');
    const chatbotSend = document.getElementById('chatbotSend');
    const chatbotClear = document.getElementById('chatbotClear');

    function addMessage(message, isBot) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');
        messageElement.classList.add(isBot ? 'bot-message' : 'user-message');
        messageElement.textContent = message;
        chatbotMessages.appendChild(messageElement);
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }

    function sendMessage() {
        const message = chatbotInput.value.trim();
        if (message) {
            addMessage(message, false);
            chatbotInput.value = '';
            chatbotInput.disabled = true;
            chatbotSend.disabled = true;

            const csrftoken = getCookie('csrftoken');

            fetch('/chat_message/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({message: message})
            })
            .then(response => {
                console.log('Response status:', response.status); // Добавим логирование
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                if (response.status === 401) {
                    window.location.href = '/login/';
                    throw new Error('Unauthorized');
                }
                return response.json();
            })
            .then(data => {
                console.log('Response data:', data); // Добавим логирование
                if (data.status === 'success') {
                    addMessage(data.message, true);
                } else {
                    addMessage('Ошибка: ' + data.message, true);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                addMessage('Произошла ошибка при отправке сообщения: ' + error.message, true);
            })
            .finally(() => {
                chatbotInput.disabled = false;
                chatbotSend.disabled = false;
                chatbotInput.focus();
            });
        }
    }

    chatbotSend.addEventListener('click', sendMessage);
    chatbotInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    if (chatbotClear) {
        chatbotClear.addEventListener('click', function() {
            fetch('/chat_message/', {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    chatbotMessages.innerHTML = '';
                    addMessage('Чат очищен. Чем я могу вам помочь?', true);
                } else {
                    console.error('Error:', data.message);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Загрузка истории сообщений при открытии страницы
    fetch('/chat_message/', {
        method: 'GET',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            data.messages.forEach(msg => addMessage(msg.message, msg.is_bot));
        } else {
            console.error('Error:', data.message);
        }
    })
    .catch(error => console.error('Error:', error));
});
