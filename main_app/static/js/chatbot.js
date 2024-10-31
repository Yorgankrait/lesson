document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chatbotMessages');
    const chatInput = document.getElementById('chatbotInput');
    const sendButton = document.getElementById('chatbotSend');
    const clearButton = document.getElementById('chatbotClear');

    addMessage("Привет! Я Кеша, ваш виртуальный помощник. Чем могу помочь?", 'bot');

    function sendMessage() {
        const message = chatInput.value.trim();
        if (message) {
            addMessage(message, 'user');
            chatInput.value = '';
            processMessage(message);
        }
    }

    function processMessage(message) {
        message = message.toLowerCase();

        if (message.includes('привет') || message.includes('здравствуй')) {
            addMessage("Здравствуйте! Рад вас видеть!", 'bot');
        }
        else if (message.includes('как войти') || message.includes('как зарегистрироваться')) {
            addMessage(`Для регистрации нажмите кнопку "Регистрация" внизу страницы. При регистрации выберите тип профиля:
            - Ученик (требует активации администратором)
            - Родитель (ограниченный доступ)
            - Учитель (требует активации администратором)
            
            После регистрации дождитесь активации профиля.`, 'bot');
        }
        else if (message.includes('учебные материалы') || message.includes('уроки')) {
            addMessage(`Доступ к учебным материалам имеют:
            - Администраторы
            - Активированные учителя
            - Активированные ученики
            
            Родители не имеют доступа к учебным материалам.`, 'bot');
        }
        else if (message.includes('кешагпт') || message.includes('keshaгпт')) {
            addMessage(`KeshaGPT доступен только для:
            - Администраторов
            - Активированных учителей`, 'bot');
        }
        else if (message.includes('полезное для учителей')) {
            addMessage(`Раздел "Полезное для учителей" доступен только для:
            - Администраторов
            - Активированных учителей
            
            В этом разделе можно создавать и просматривать статьи с полезными материалами.`, 'bot');
        }
        else if (message.includes('проекты') || message.includes('ученики')) {
            addMessage("Раздел 'Ученики и их проекты' доступен всем пользователям. Здесь можно увидеть информацию об учениках и их проектах.", 'bot');
        }
        else if (message.includes('интерпретатор') || message.includes('python')) {
            addMessage("Python Интерпретатор доступен всем пользователям. Здесь можно писать и выполнять код на Python прямо в браузере.", 'bot');
        }
        else {
            addMessage("Извините, я не совсем понял ваш вопрос. Попробуйте спросить о регистрации, доступе к материалам, проектах учеников или других функциях сайта.", 'bot');
        }
    }

    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender);
        messageDiv.textContent = text;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    sendButton.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    if (clearButton) {
        clearButton.addEventListener('click', function() {
            chatMessages.innerHTML = '';
            addMessage("Чат очищен. Чем могу помочь?", 'bot');
        });
    }
}); 