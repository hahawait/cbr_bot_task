# Инструкция по настройке окружения и запуску проекта

1. Создайте файл `bot/.env`:
    ```plaintext
    # Redis
    REDIS_HOST=redis # for docker
    # REDIS_HOST=localhost
    REDIS_PORT=6379

    # Bot
    BOT_TOKEN=ВАШ_ТОКЕН_ЗДЕСЬ
    ```

2. Получите токен для бота и поместите его в файл `bot/.env`, заменив `ВАШ_ТОКЕН_ЗДЕСЬ` на реальный токен.

3. Создайте файл `bank/.env`.
    ```plaintext
    # API
    URL=https://cbr.ru
    EXCHANGE_RATES_ENDPOINT=/scripts/XML_daily.asp

    # Redis
    REDIS_HOST=redis # for docker
    # REDIS_HOST=localhost
    REDIS_PORT=6379
    ```

4. Запустите `docker-compose`:
    ```sh
    docker-compose up
    ```