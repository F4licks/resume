#!/bin/bash

# Определите путь к файлу со списком IP-адресов
IP_FILE="Ip.txt"
user='kabinet202'
# Проверяем, существует ли файл
if [ ! -f "$IP_FILE" ]; then
    echo "Файл $IP_FILE не найден!"
    exit 1
fi

# Читаем список IP-адресов из файла
ip_list=()
while IFS= read -r line; do
    ip_list+=("$line")
done < "$IP_FILE"

# Запрашиваем у пользователя настройку прокси
read -p "Введите '1' для прямого подключения (none) или '2' для ручной настройки (manual): " user_input

# Функция для настройки прокси на удаленном ПК
set_proxy() {
    local ip=$1
    local mode=$2

    if [ "$mode" == "2" ]; then
        echo "Переключение на ручную настройку прокси на $ip..."
        
        # Устанавливаем режим прокси на 'manual'
        ssh $user@"$ip" "gsettings set org.gnome.system.proxy mode 'manual' && 
                         gsettings set org.gnome.system.proxy.http host '10.0.50.52' && 
                         gsettings set org.gnome.system.proxy.http port 3128 && 
                         gsettings set org.gnome.system.proxy.https host '10.0.50.52' && 
                         gsettings set org.gnome.system.proxy.https port 3128"

        echo "Ручная настройка прокси включена на $ip."
    elif [ "$mode" == "1" ]; then
        echo "Переключение на прямое соединение на $ip..."

        # Устанавливаем режим прокси на 'none'
        ssh $user@"$ip" "gsettings set org.gnome.system.proxy mode 'none'"

        echo "Прямое соединение с интернетом включено на $ip."
    else
        echo "Некорректный ввод. Прокси не будет настроен на $ip."
    fi
}

# Применяем настройки прокси к каждому IP-адресу
for ip in "${ip_list[@]}"; do
    set_proxy "$ip" "$user_input"
done

echo "Настройки прокси применены ко всем IP-адресам в списке."
