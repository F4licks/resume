#!/bin/bash

# Проверяем текущие настройки прокси
current_proxy=$(gsettings get org.gnome.system.proxy mode)

if [ "$current_proxy" == "'none'" ]; then
    echo "Переключение на ручную настройку прокси..."

# Устанавливаем режим прокси на 'manual'
    gsettings set org.gnome.system.proxy mode 'manual'

# Устанавливаем адреса прокси(!!!замените на ваши!!!)
    gsettings set org.gnome.system.proxy.http host 'proxy.example.com'
    gsettings set org.gnome.system.proxy.http port 8080
    gsettings set org.gnome.system.proxy.https host 'proxy.example.com'
    gsettings set org.gnome.system.proxy.https port 8080

    echo "Ручная настройка прокси включена."
else
    echo "Переключение на прямое соединение..."

# Устанавливаем режим прокси на 'none'
    gsettings set org.gnome.system.proxy mode 'none'

    echo "Прямое соединение с интернетом включено."
fi

