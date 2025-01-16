#!/bin/bash

KEY_PATH="$HOME/.ssh/id_rsa.pub"  #Путь к публичному SSH ключу
IP_L="Ip.txt"         #Файл со списком IP адресов

#Проверка наличия SSH ключа
if [ ! -f "$KEY_PATH" ]; then
    echo "SSH ключ не найден. Генерируем новый ключ"
    ssh-keygen -t rsa -b 2048 -f "$HOME/.ssh/id_rsa" -N ""
else
    echo "SSH ключ найден."
fi

#Чтение IP адресов из файла
if [ ! -f "$IP_L" ]; then
    echo "Файл со списком IP адресов не найден!"
    exit 1
fi

for ip in $(cat $IP_L); do
    echo "Проверяем доступность $ip"

    #Проверка доступности хоста
    if ping -c 1 "$ip" &> /dev/null; then
        echo "$ip доступен."

        #Проверка наличия SSH ключа на удаленной машине
        ssh -o BatchMode=yes -o ConnectTimeout=5 "$ip" exit &> /dev/null

        if [ $? -eq 0 ]; then
            echo "SSH ключ уже скопирован на $ip."
        else
            echo "Ключ не скопирован на $ip. Копируем"
            ssh-copy-id "$ip"
        fi
    else
        echo "$ip недоступен."
    fi
done

echo "Завершено."

