# Manual Git — Soporte Técnico

## ¿Qué es Git?
Git es un sistema de control de versiones distribuido para registrar cambios en archivos y colaborar en equipo.

## Configuración inicial
```
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```

## Cómo clonar un repositorio
```
git clone https://github.com/usuario/repositorio.git
```

## Cómo actualizar un repositorio Git
Para actualizar el repositorio local con cambios remotos:

```
git pull origin main
```

Forma más controlada:
```
git fetch origin
git merge origin/main
```

Actualizar todas las ramas:
```
git fetch --all
```

Si hay conflictos durante el pull:
1. Git marcará los archivos con conflicto.
2. Abrir los archivos y resolver manualmente.
3. `git add archivo-resuelto.txt`
4. `git commit`

## Flujo básico de trabajo
```
git status
git add .
git commit -m "descripción"
git push origin main
```

## Manejo de ramas
```
git branch                  # listar ramas
git branch nueva-rama       # crear rama
git checkout nueva-rama     # cambiar de rama
git checkout -b nueva-rama  # crear y cambiar
git merge rama-origen       # fusionar rama
git branch -d rama          # eliminar rama local
```

## Deshacer cambios
```
git restore archivo.txt     # descartar cambios
git reset HEAD~1            # deshacer último commit
git revert HEAD             # revertir con nuevo commit
```

## Ver historial
```
git log --oneline
git log --oneline --graph
git diff
```

## Stash
```
git stash        # guardar cambios temporalmente
git stash pop    # recuperar cambios
git stash list   # listar stashes
```
