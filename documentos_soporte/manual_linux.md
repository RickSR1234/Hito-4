# Manual Linux — Soporte Técnico

## Navegación
```
pwd       # directorio actual
ls -la    # listar con detalle
cd /ruta  # cambiar directorio
cd ~      # ir a home
```

## Gestión de archivos
```
mkdir carpeta
rm archivo.txt
rm -rf carpeta/
cp origen destino
mv origen destino
cat archivo.txt
tail -f log.txt
```

## Cómo visualizar procesos en Linux

Para ver procesos en ejecución:

**ps — instantánea:**
```
ps aux
ps aux | grep nginx
```
Columnas: USER, PID, %CPU, %MEM, COMMAND

**top — monitor interactivo:**
```
top
```
Dentro de top: q=salir, k=terminar proceso, M=ordenar por memoria, P=ordenar por CPU

**htop — monitor mejorado:**
```
htop
```

**Filtrar por nombre:**
```
pgrep nginx
pidof apache2
```

## Terminar procesos
```
kill PID
kill -9 PID
killall nombre
```

## Servicios con systemd
```
systemctl status nginx
systemctl start nginx
systemctl stop nginx
systemctl restart nginx
journalctl -u nginx -f
```

## Disco y memoria
```
df -h
du -sh /ruta
free -h
```

## Red
```
ip addr
ping host
ss -tuln
curl -I https://url
```

## Permisos
```
chmod 755 archivo
chmod +x script.sh
chown usuario:grupo archivo
sudo comando
```

## Búsqueda
```
find /ruta -name "*.log"
grep "patron" archivo.txt
grep -r "patron" /ruta/
```
