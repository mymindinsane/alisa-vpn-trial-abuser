# Alisa Trial Abuse Tester

Консольная версия Alisa Trial Abuse Tester.

Она открывает страницу регистрации в Chromium, вводит email и пароль, выбирает
Windows и выводит полученную VPN-ссылку в терминал.

## Важно

Проект предоставляется в образовательных целях и должен использоваться только
на сайтах, системах и аккаунтах, где у вас есть разрешение на автоматизацию. Не
используйте его для обхода лимитов сервисов, нарушения правил, создания
несанкционированных аккаунтов или доступа без разрешения.

## Требования

- Python 3.9 или новее
- Playwright для Python
- Playwright Chromium

## Установка

Создайте и активируйте виртуальное окружение:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Установите зависимости:

```powershell
pip install playwright
python -m playwright install chromium
```

## Запуск

Запуск с настройками по умолчанию:

```powershell
python .\register_vpn_link.py
```

Пример вывода:

```text
Generated email: qwerty_ab12cd34@mail.ru
https://sub.example.com/example_link
```

Первая строка - сгенерированный email. Вторая строка - полученная ссылка.

## Показать Браузер

Используйте `--headful`, чтобы видеть окно браузера во время работы скрипта:

```powershell
python .\register_vpn_link.py --headful
```

Это удобно, если нужно понять, на каком шаге останавливается сценарий.

## Переопределить Настройки

В `register_vpn_link.py` есть значения по умолчанию, но их можно
переопределить для одного запуска.

Использовать другой пароль:

```powershell
python .\register_vpn_link.py --password "AnotherPassword123"
```

Использовать другой домен email:

```powershell
python .\register_vpn_link.py --email-domain "mail.com"
```

Переопределить несколько значений:

```powershell
python .\register_vpn_link.py `
  --email-prefix "qwerty" `
  --email-domain "mail.com" `
  --device-text "Windows" `
  --timeout-ms 45000
```

## Параметры

Все параметры необязательные.

| Параметр | Значение |
| --- | --- |
| `--url` | URL страницы регистрации |
| `--password` | Пароль, который вводится в форму |
| `--email-prefix` | Префикс для сгенерированного email |
| `--email-domain` | Домен для сгенерированного email |
| `--device-text` | Текст для выбора Windows |
| `--headful` | Показывает окно браузера |
| `--timeout-ms` | Максимальное время ожидания действий на странице |
| `--email-selector` | Селектор поля email |
| `--password-selector` | Селектор поля пароля |
| `--submit-selector` | Селектор кнопки отправки формы |
| `--link-selector` | Необязательный селектор поля со ссылкой |
| `--copied-selector` | Необязательный селектор дополнительной кнопки после шага со ссылкой |

## Поиск Ссылки

Если `--link-selector` не указан, скрипт ищет ссылку в:

- `input`
- `textarea`
- `code`
- `pre`
- `a`
- видимом тексте страницы

Если ссылка всегда находится в известном элементе, передайте селектор:

```powershell
python .\register_vpn_link.py --link-selector "input"
```

## Решение Проблем

Если вариант Windows не найден, скрипт сохраняет:

```text
no_windows_card_found.png
```

Если ссылка не найдена, скрипт сохраняет:

```text
no_vpn_link_found.png
```

Откройте скриншот, чтобы увидеть, что было показано в браузере во время ошибки.

## Лицензия

MIT License - распространенный вариант для небольшого скрипта.

Важно: лицензия не делает неправильное использование законным. Она только
описывает, как другие могут копировать, изменять и распространять код.
