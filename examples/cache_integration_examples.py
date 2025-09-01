"""
Примеры интеграции Redis кеширования в существующие хендлеры Telegram бота
"""

from database.cache_decorators import cache_result, cache_user_data, cache_invalidate
from database.redis_cache import get_cache


# Пример 1: Кеширование профиля пользователя
@cache_user_data(ttl=1800)  # 30 минут
async def get_user_profile(message):
    """
    Получение профиля пользователя с кешированием.
    Кеш автоматически инвалидируется при изменении данных пользователя.
    """
    # Здесь будет ваш код получения профиля из БД
    user_id = message.from_user.id
    # ... получение данных из БД
    return {"user_id": user_id, "profile_data": "..."}


# Пример 2: Кеширование списка администраторов
@cache_result(key_prefix="admins", ttl=3600)  # 1 час
async def get_admin_users():
    """
    Получение списка администраторов с кешированием.
    Кеш обновляется каждый час или при изменении статуса администратора.
    """
    # ... получение списка администраторов из БД
    return [123456789, 987654321]


# Пример 3: Кеширование статистики бота
@cache_result(key_prefix="bot_stats", ttl=900)  # 15 минут
async def get_bot_statistics():
    """
    Получение статистики бота с кешированием.
    Обновляется каждые 15 минут для актуальности данных.
    """
    # ... расчет статистики
    return {
        "total_users": 1000,
        "active_users": 500,
        "total_subscriptions": 100
    }


# Пример 4: Кеширование настроек группы
@cache_result(key_prefix="group_settings", ttl=7200)  # 2 часа
async def get_group_settings(chat_id: int):
    """
    Получение настроек группы с кешированием.
    Кешируется по chat_id для каждой группы отдельно.
    """
    # ... получение настроек группы из БД
    return {"chat_id": chat_id, "settings": "..."}


# Пример 5: Кеширование с инвалидацией
@cache_invalidate(pattern="user:*")
async def update_user_profile(message, new_data):
    """
    Обновление профиля пользователя с автоматической инвалидацией кеша.
    После обновления все кешированные данные пользователя будут очищены.
    """
    user_id = message.from_user.id
    
    # ... обновление данных в БД
    
    # Кеш автоматически инвалидируется благодаря декоратору
    return {"success": True, "user_id": user_id}


# Пример 6: Кеширование с кастомным ключом
@cache_result(key_prefix="subscription", ttl=1800)
async def get_user_subscription_status(user_id: int):
    """
    Получение статуса подписки пользователя с кешированием.
    Кешируется по user_id на 30 минут.
    """
    # ... получение статуса подписки из БД
    return {"user_id": user_id, "subscription_active": True, "expires_at": "..."}


# Пример 7: Кеширование результатов сложных вычислений
@cache_result(key_prefix="analytics", ttl=3600)
async def calculate_user_analytics(user_id: int, period: str = "month"):
    """
    Кеширование результатов сложных аналитических вычислений.
    Кеш обновляется каждый час.
    """
    # ... сложные вычисления аналитики
    return {
        "user_id": user_id,
        "period": period,
        "usage_stats": "...",
        "recommendations": "..."
    }


# Пример 8: Условное кеширование
async def get_user_data_with_conditional_cache(message):
    """
    Пример условного кеширования в зависимости от условий.
    """
    user_id = message.from_user.id
    cache = await get_cache()
    
    # Проверяем, есть ли данные в кеше
    cached_data = await cache.get(f"user_data:{user_id}")
    if cached_data:
        return cached_data
    
    # Если данных нет в кеше, получаем из БД
    user_data = await fetch_user_data_from_db(user_id)
    
    # Кешируем только если пользователь активен
    if user_data.get("is_active"):
        await cache.set(f"user_data:{user_id}", user_data, ttl=1800)
    
    return user_data


# Пример 9: Кеширование с приоритетами
async def get_priority_data(data_type: str, priority: str = "normal"):
    """
    Кеширование с разными TTL в зависимости от приоритета данных.
    """
    cache = await get_cache()
    
    # Определяем TTL в зависимости от приоритета
    ttl_map = {
        "high": 300,      # 5 минут для высокоприоритетных данных
        "normal": 1800,   # 30 минут для обычных данных
        "low": 7200       # 2 часа для низкоприоритетных данных
    }
    
    ttl = ttl_map.get(priority, 1800)
    
    # Проверяем кеш
    cache_key = f"priority_data:{data_type}:{priority}"
    cached_data = await cache.get(cache_key)
    if cached_data:
        return cached_data
    
    # Получаем данные из БД
    data = await fetch_data_from_db(data_type)
    
    # Кешируем с соответствующим TTL
    await cache.set(cache_key, data, ttl=ttl)
    
    return data


# Пример 10: Кеширование с автоматической очисткой
async def cache_user_session_data(user_id: int, session_data: dict):
    """
    Кеширование сессионных данных пользователя с автоматической очисткой.
    """
    cache = await get_cache()
    
    # Кешируем сессионные данные на короткое время
    session_key = f"user_session:{user_id}"
    await cache.set(session_key, session_data, ttl=300)  # 5 минут
    
    # Также кешируем основные данные пользователя на более долгое время
    user_key = f"user_data:{user_id}"
    await cache.set(user_key, session_data.get("user_info"), ttl=3600)  # 1 час
    
    return True


# Пример 11: Кеширование с обработкой ошибок
async def safe_cache_get(key: str, fallback_func, ttl: int = 1800):
    """
    Безопасное получение данных из кеша с fallback функцией.
    """
    try:
        cache = await get_cache()
        
        # Пытаемся получить из кеша
        cached_data = await cache.get(key)
        if cached_data is not None:
            return cached_data
        
        # Если в кеше нет, вызываем fallback функцию
        data = await fallback_func()
        
        # Кешируем результат
        await cache.set(key, data, ttl=ttl)
        
        return data
        
    except Exception as e:
        # В случае ошибки кеширования, просто возвращаем данные без кеша
        print(f"Ошибка кеширования: {e}")
        return await fallback_func()


# Пример 12: Кеширование с метаданными
async def cache_with_metadata(key: str, data: dict, metadata: dict = None):
    """
    Кеширование данных с дополнительными метаданными.
    """
    cache = await get_cache()
    
    # Добавляем метаданные к данным
    cache_data = {
        "data": data,
        "metadata": metadata or {},
        "cached_at": "2024-01-01T00:00:00Z",
        "version": "1.0"
    }
    
    # Кешируем данные с метаданными
    await cache.set(key, cache_data, ttl=3600)
    
    return True


# Пример 13: Кеширование с инкрементальными обновлениями
async def increment_user_counter(user_id: int, counter_type: str):
    """
    Инкрементальное обновление счетчиков пользователя с кешированием.
    """
    cache = await get_cache()
    
    cache_key = f"user_counter:{user_id}:{counter_type}"
    
    # Пытаемся получить текущее значение из кеша
    current_value = await cache.get(cache_key)
    
    if current_value is None:
        # Если в кеше нет, получаем из БД
        current_value = await get_counter_from_db(user_id, counter_type)
    
    # Увеличиваем значение
    new_value = current_value + 1
    
    # Обновляем кеш
    await cache.set(cache_key, new_value, ttl=7200)  # 2 часа
    
    # Также обновляем в БД
    await update_counter_in_db(user_id, counter_type, new_value)
    
    return new_value


# Пример 14: Кеширование с группировкой
async def get_grouped_user_data(group_id: str):
    """
    Кеширование сгруппированных данных пользователей.
    """
    cache = await get_cache()
    
    cache_key = f"grouped_users:{group_id}"
    
    # Проверяем кеш
    cached_data = await cache.get(cache_key)
    if cached_data:
        return cached_data
    
    # Получаем данные из БД
    users_data = await fetch_users_by_group(group_id)
    
    # Группируем данные
    grouped_data = {}
    for user in users_data:
        status = user.get("status", "unknown")
        if status not in grouped_data:
            grouped_data[status] = []
        grouped_data[status].append(user)
    
    # Кешируем сгруппированные данные
    await cache.set(cache_key, grouped_data, ttl=1800)
    
    return grouped_data


# Пример 15: Кеширование с автоматическим обновлением
async def get_auto_refresh_data(key: str, fetch_func, ttl: int = 1800):
    """
    Кеширование с автоматическим обновлением данных в фоне.
    """
    cache = await get_cache()
    
    # Проверяем кеш
    cached_data = await cache.get(key)
    if cached_data:
        # Если данные есть в кеше, запускаем обновление в фоне
        asyncio.create_task(refresh_cache_background(key, fetch_func, ttl))
        return cached_data
    
    # Если данных нет, получаем и кешируем
    data = await fetch_func()
    await cache.set(key, data, ttl=ttl)
    
    return data


async def refresh_cache_background(key: str, fetch_func, ttl: int):
    """
    Фоновое обновление кеша.
    """
    try:
        cache = await get_cache()
        
        # Получаем новые данные
        new_data = await fetch_func()
        
        # Обновляем кеш
        await cache.set(key, new_data, ttl=ttl)
        
        print(f"Кеш {key} обновлен в фоне")
        
    except Exception as e:
        print(f"Ошибка при фоновом обновлении кеша {key}: {e}")


# Пример использования в хендлере
async def example_handler(message):
    """
    Пример использования кеширования в хендлере Telegram бота.
    """
    user_id = message.from_user.id
    
    try:
        # Получаем профиль пользователя (закеширован)
        profile = await get_user_profile(message)
        
        # Получаем статистику (закеширована)
        stats = await get_bot_statistics()
        
        # Получаем статус подписки (закеширован)
        subscription = await get_user_subscription_status(user_id)
        
        # Формируем ответ
        response = f"""
👤 Профиль: {profile}
📊 Статистика: {stats}
💎 Подписка: {subscription}
        """
        
        return response
        
    except Exception as e:
        print(f"Ошибка в хендлере: {e}")
        return "Произошла ошибка при получении данных"
