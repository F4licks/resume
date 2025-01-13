#!/bin/bash
pol=$(whoami)
rm -rf /home/$pol/Видео/*
rm -rf /home/$pol/Загрузки/*
rm -rf /home/$pol/Изображения/*
rm -rf /home/$pol/Музыка/*
rm -rf ~/.local/share/Trash/files/* 
rm -rf ~/.local/share/Trash/info/*
sudo dnf makecache
sudo dnf upgrade -y
sudo poweroff
