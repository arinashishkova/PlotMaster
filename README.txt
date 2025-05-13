# PlotMaster

Управление сюжетом и персонажами для писателей и сценаристов.

![Build Status](https://img.shields.io/github/actions/workflow/status/YourUser/PlotMaster/ci.yml)
![Coverage](https://img.shields.io/codecov/c/github/YourUser/PlotMaster)

## Содержание

1. [Описание](#описание)  
2. [Требования](#требования)  
3. [Установка](#установка)  
4. [Использование](#использование)  
5. [Тестирование](#тестирование)  
6. [Seed данных](#seed-данных)  
7. [Структура проекта](#структура-проекта)  
8. [Контрибьютинг](#контрибьютинг)  
9. [Лицензия](#лицензия)

---

## Описание

PlotMaster — настольное PyQt5-приложение для управления сценариями, персонажами, событиями и связями между ними.

## Требования

- Python 3.10+  
- PyQt5  
- Peewee  

## Установка

```bash
# клонируем репозиторий
git clone https://github.com/YourUser/PlotMaster.git
cd PlotMaster

# создаём venv
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\Activate.ps1  # Windows PowerShell

# устанавливаем зависимости
pip install -r requirements.txt
pip install -r requirements-dev.txt  # для запуска тестов
