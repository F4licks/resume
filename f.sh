#!/bin/bash

# Создание файла /etc/sudoers.d/kabinet202, если он не существует
pol=$(whoami)
if [ ! -f /etc/sudoers.d/$pol ]; then
    sudo touch /etc/sudoers.d/$pol
fi

# Проверка и добавление строки, если она отсутствует
if ! grep -q "$pol ALL=(ALL) NOPASSWD:ALL" /etc/sudoers.d/$pol; then
    echo "$pol ALL=(ALL) NOPASSWD:ALL" | sudo tee -a /etc/sudoers.d/$pol > /dev/null
    echo "Запись добавлена в /etc/sudoers.d/$pol"
else
    echo "Запись уже существует!"
fi

# Установка правильных прав для файла
sudo chmod 440 /etc/sudoers.d/$pol
# устанавливаем время работы
(crontab -l; echo "00 17 * * * /home/clean.sh") | crontab -
sudo mv clean.sh /home
sudo mv f.sh /home
sudo chmod +x /home/clean.sh
