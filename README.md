# final qualifying work
Flask + Vue3

## Установка
```bash
git clone https://github.com/HeAmongUs/FinalQualifyingWork
cd backend
python -r requirements.txt
cd .. && cd frontend
npm i
```

## Подсистема аутентификации
### Аутентификация на основе JWT
PyJWT + реализован класс my_jwt со @staticmethod:
- def encode_token(username: str, token_type: str = "access", ) -> str:
- def decode_token(token: str, token_type: str = "access", ) -> dict:
- def jwt_required(token_type="access"):
- def get_username_from_jwt(token: str, token_type: str = 'access') -> str:
- def get_current_user(token_type: str = 'access') -> User:
- def get_token_from_request(token_type='access'):

### Аутентификация по OTP на email в качестве 2FA
Для отправки письма используется пакет Flask-Mail
Для генерации пароля модуль secrets стандартной библиотеки для генерации криптографически стойкой последовательности псевдослучайнх чисел

### Хэширование пароля
SHA-256 + "соль" генерируемая модулем secrets

### Требования к сложности пароля
В настройках приожения:
- PASSWORD_MIN_LENGTH = 6
- PASSWORD_INCLUDES_SPECIAL_SYMBOLS = True
- PASSWORD_INCLUDES_LOWERCASE = True
- PASSWORD_INCLUDES_UPPERCASE = True
- PASSWORD_INCLUDES_DIGITS = True

Для проверки выполнения требований и проверки вводимых значений при создании пользователя создан класс UserValidator
