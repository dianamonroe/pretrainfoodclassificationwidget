#!/bin/bash



# Dirección de tu Codespace (puedes usar localhost:8000 si tienes un servidor Flask o similar corriendo)
URL="https://5000-dianamonroe-pretrainfoo-5kxfosndqx6.ws-eu117.gitpod.io"


echo "Manteniendo el Codespace activo con intervalos dinámicos entre 3 y 95 segundos."

while true; do
    # Realizar una solicitud para evitar la desconexión
    curl -s $URL > /dev/null
    echo "Solicitud enviada a $URL"
    
    # Generar un intervalo dinámico entre 3 y 95 segundos
    INTERVAL=$((3 + RANDOM % 93))
    echo "Esperando $INTERVAL segundos antes de la próxima solicitud."
    
    # Esperar antes de la siguiente solicitud
    sleep $INTERVAL
done
