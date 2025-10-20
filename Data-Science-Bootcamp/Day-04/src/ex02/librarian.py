import os
import subprocess
import sys

def check_venv():
    venv_path = os.environ.get('VIRTUAL_ENV')

    if venv_path is None or "anjabeve" not in venv_path:
        raise EnvironmentError('Not running in correct a virtual environment! \nCorrect env name: "anjabeve"')
    else:
        print("Correct environment!")
        

def install_libs():
    packages = ['beautifulsoup4', 'pytest', 'termgraph', 'zipp']
    
    try:
        subprocess.run(['pip', 'install', *packages], check=True)
    except subprocess.CalledProcessError as e:
        print("Error installing packages!")
        print("Command:", e.cmd)
        print("Exit code:", e.returncode)
    
def list_libs():
    result = subprocess.run(["pip", "freeze"], capture_output=True, text=True)
    print(result.stdout)

def save_to_requirements():
    subprocess.run('pip freeze > requirements.txt', shell=True, check=True, capture_output=True, text=True)
    print("Saved installed packages to requirements.txt")   

if __name__ == "__main__":
    try:
        check_venv()
    except EnvironmentError as e:
        print(e)
        sys.exit(1)

    install_libs()
    list_libs()
    save_to_requirements()
