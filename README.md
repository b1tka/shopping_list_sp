Shopping List
===================================
>Telegram Bot/School Project/Shopping List

Школьный проект по информатике
----------------------------
Tg бот список покупок
--------------------------
Что планирую реализовать
-----------------------
- Создание групп
- Динамический список покупок
- Индивидуальные рассылки с напоминанием

БД
-----------------------
- users
  - user_id (Primary key)
  - nickname (STRING)
  - personal_time (TIME)

- group
  - group_id (Primary key)
  - group_code (VARCHAR)
  - admin_id (INTEGER)
  - member_id (INTEGER)
  - lists_id (INTEGER)

- lists
  - list_id (Primary key)
  - item (STRING)
  - smth_has_bought (BOOLING)

Tехническое задание (ТЗ)
--------------------------
- [ ] Создание БД
  - [ ] Создание таблицы user
  - [ ] Создание таблицы group
  - [ ] Создание таблицы lists
- [ ] Создание API с пользователем
  - [ ] Подключение БД
  - [ ] Возможность создать/подключиться к группе
  - [ ] Реализация списка покупок
  - [ ] Реализация индивидуальных уведомлений пользователю
- [ ] Написание теоритической части
  - [ ] Введение
  - [ ] Основная часть
  - [ ] Заключение 
