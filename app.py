import asyncio
import subprocess
import os
import time
import json
import requests
import base64
import platform
import shutil
import psutil
import config as config

repo_path = config.app.repoPath
running_port = config.app.runningPort
child_process = None

def run_command(command, options={}):
    if platform.system() == 'Windows':
        command_args = [command]
    
    elif platform.system() == 'Linux':
        command_args = ['gnome-terminal', '--', 'bash', '-c', command]

    else:
        print("Sistema operativo no soportado.")
        return None

    process = subprocess.Popen(command_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **options)
    stdout, stderr = process.communicate()

    if stdout:
        print(f"stdout: {stdout.decode('utf-8')}")
    if stderr:
        print(f"stderr: {stderr.decode('utf-8')}")
    print(f"Proceso hijo finalizado con código de salida {process.returncode}")
    return process

async def check_changes():
    try:
        print(f"[{time.strftime('%H:%M:%S')}]", "Checking updates...")
        response = requests.get(
            f"https://api.github.com/repos/{config.github.username}/{config.github.repoName}/contents/package.json",
            headers={
                'Accept': 'application/vnd.github.v3+json',
                'Authorization': f"token {config.github.token}"
            }
        )
        content = base64.b64decode(response.json()['content']).decode('utf-8')
        package_json_version_remote = json.loads(content)['version']
        with open(os.path.join(repo_path, 'package.json'), 'r') as f:
            package_json_version_local = json.load(f)['version']
        return (package_json_version_local == package_json_version_remote)
    except Exception as e:
        print('Error al ver actualizacion:', e)
        return False

def kill_processes_on_port(port):
    for process in psutil.process_iter(['pid', 'name', 'connections']):
        try:
            connections = process.info.get('connections')
            if connections is None:
                continue

            for conn in connections:
                if conn.laddr.port == port:
                    print(f"Terminando proceso {process.pid}: {process.info['name']}")
                    process.terminate()
                    break
        except psutil.AccessDenied:
            continue

def init_app():
    print(f"STARTING {config.github.repoName} ##################################")
    global child_process
    child_process = run_command(config.app.runCommand, options={'cwd': repo_path})

def delete_folder(folder_path):
    try:
        shutil.rmtree(folder_path)
        print(f"Folder {folder_path} deleted successfully.")
    except OSError as e:
        print(f"Failed to delete folder {folder_path}: {e}")

def delete_build_folder():
    delete_folder(repo_path + "/" + config.app.buildFolderName)

def pull_app():
    print("PULLING CHANGES ###################################")
    run_command('git pull', options={'cwd': repo_path})

def build_app():
    print("BUILDING CHANGES ###################################")
    run_command('npm run build', options={'cwd': repo_path})

async def loop():
    is_updated = await check_changes()
    if not is_updated:
        print("UPDATES AVAILABLE #############################")
        kill_processes_on_port(config.app.runningPort)
        time.sleep(5)
        delete_build_folder()
        time.sleep(5)
        pull_app()
        time.sleep(5)
        build_app()
        time.sleep(20)
        await start_app()
    else:
        await asyncio.sleep(10)
        await loop()


async def start_app():
    init_app()
    time.sleep(5)
    await loop()

async def main():
    await start_app()

if __name__ == "__main__":
    asyncio.run(main())
