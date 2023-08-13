# Описание консольной программы Appnote

Appnote - это консольная программа для создания и управления заметками. С помощью этой программы пользователь может создавать, просматривать, редактировать и удалять заметки.

## Использование

При запуске программы пользователю будет предложено выбрать действие:

- Создать новую заметку
- Просмотреть список заметок
- Выход из программы

При промстре списка заметок, выбрав нужную заметку, откроется:
- Содержимое заметки
- Редактировать заметку
- Удалить заметку
- Вернуться к списку заметок

### Создание новой заметки

При выборе этого действия пользователь будет попросен ввести заголовок и содержимое заметки. Пустые поля недопустимы. После ввода заметка будет сохранена в файле с уникальным номером в папке Data в файле notes.json.

### Просмотр списка заметок

При выборе этого действия пользователь увидит список всех созданных заметок. Каждая заметка будет представлена своим заголовком и датой изменения.

### Просмотр содержимого заметки

При выборе этого действия на экран будет выведено содержимое выбранной заметки и дополнительное меню.

### Редактирование заметки

При выборе этого действия пользователь сможет отредактировать заголовок и содержимое заметки.

### Удаление заметки

При выборе этого действия пользователь должен повторно подтвердить его. После этого выбранная заметка будет удалена.

### Выход из программы

При выборе этого действия и повторного подтверждения программа завершится.

## Технические детали

Программа написана на языке Python 3 с использованием модуля os для сохранения и загрузки файлов. Заметки хранятся в формате json. Интерфейс программы реализован в виде консольного меню. При желании можно переключиться на меню команд, заменив в main экземпляр класса ConsoleUI на TextCommandUI. В данном реджиме все доступные команды выведутся на экран при запуске программы.  