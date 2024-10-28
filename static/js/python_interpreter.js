document.addEventListener('DOMContentLoaded', function() {
    const codeEditor = CodeMirror.fromTextArea(document.getElementById('code'), {
        mode: 'python',
        theme: 'dracula',
        lineNumbers: true,
        autoCloseBrackets: true,
        matchBrackets: true,
        indentUnit: 4,
        tabSize: 4,
        indentWithTabs: false,
        extraKeys: {
            "Tab": function(cm) {
                cm.replaceSelection("    ", "end");
            },
            "Shift-Enter": runCode,  // Добавляем горячую клавишу
        }
    });

    const runButton = document.getElementById('runCode');
    const output = document.getElementById('output');

    runButton.addEventListener('click', runCode);

    function runCode() {
        const code = codeEditor.getValue();
        
        fetch('/run-python-code/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({code: code})
        })
        .then(response => response.json())
        .then(data => {
            output.textContent = data.output;
        })
        .catch(error => {
            console.error('Error:', error);
            output.textContent = 'Произошла ошибка при выполнении кода.';
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

    // Добавляем обработчик клавиш для всего документа
    document.addEventListener('keydown', function(e) {
        // Проверяем, что фокус находится в редакторе кода
        if (document.activeElement === codeEditor.getInputField()) {
            if (e.key === 'Enter' && (e.shiftKey || e.metaKey)) {
                e.preventDefault(); // Предотвращаем стандартное поведение
                runCode();
            }
        }
    });
});
