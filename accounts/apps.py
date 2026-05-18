from django.apps import AppConfig  # Импорт базового класса конфигурации приложения

class AccountsConfig(AppConfig):  # Создаём класс конфигурации для приложения accounts
    
    default_auto_field = 'django.db.models.BigAutoField'  

    
    name = 'accounts'  
    
    verbose_name = 'Аккаунты'  
