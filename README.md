# Aplicación de Actualización Automática de Repositorios

Este es un programa Python diseñado para facilitar la gestión automática de repositorios en GitHub. El programa está especialmente adaptado para el desarrollo de aplicaciones web, donde se espera un flujo constante de cambios en el repositorio.

## Funcionalidades Principales

- **Detección de Cambios Automática:** El programa verifica periódicamente si hay cambios en el repositorio remoto en GitHub.
- **Actualización Automática:** En caso de detectar cambios, el programa realiza automáticamente las siguientes acciones:
  1. Detiene cualquier proceso que se esté ejecutando en el puerto especificado.
  2. Elimina la carpeta build existente.
  3. Obtiene los últimos cambios del repositorio remoto.
  4. Hace una nueva build de la aplicación.
  5. Inicia la aplicación actualizada.

## Requisitos

- Python 3.x
- Acceso a Internet para verificar cambios en GitHub
- Dependencias especificadas en el archivo `requirements.txt`
- Acceso al repositorio remoto en GitHub

## Configuración

El programa requiere una configuración mínima antes de su uso. Se deben establecer los siguientes parámetros en el archivo `config.py`:

1. `repoPath`: La ruta local del repositorio clonado.
2. `runningPort`: El puerto en el que se ejecutará la aplicación.
3. `app.runCommand`: El comando para ejecutar la aplicación.
4. Detalles de la cuenta de GitHub, incluido el token de acceso, para poder realizar operaciones en el repositorio remoto.

## Uso

1. Clona este repositorio en tu máquina local.
2. Instala las dependencias utilizando `pip install -r requirements.txt`.
3. Configura los parámetros necesarios en el archivo `config.py`.
4. Ejecuta el programa utilizando `python main.py`.
