import os
import json
import time
import shutil
import argparse
import subprocess

print("Python -> Updating Packages")

class MessageError(Exception):
    """Custom exception for specific error conditions."""
    pass

def clone_and_rename_original_package():
    src = './package.json'
    dst = './package.original.json'
    shutil.copy2(src, dst)

def remove_node_modules_folder():
    dir_path = './node_modules'

    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
        print(f'Directory {dir_path} and all its contents have been removed.')
    else:
        print(f'Directory {dir_path} does not exist.')

def remove_yarn_lock_file():
    file_path = './yarn.lock'

    if os.path.exists(file_path):
        os.remove(file_path)
        print(f'File {file_path} has been removed.')
    else:
        print(f'File {file_path} does not exist.')

def execute_command( command: list ):
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    
    print('stdout:', result.stdout)
    print('stderr:', result.stderr)
    print('Return code:', result.returncode)

def clear_console():
    if os.name == 'nt':  # For Windows
        execute_command(command = ['powershell', '-Command', 'clear'])
    else:  # For Unix/Linux/MacOS
        execute_command(['clear'])

def read_package_file( file_path: str ):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    
        print(f"The file {file_path} read correctly")
        return data
            
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
    except json.JSONDecodeError:
        print(f"Failed to decode JSON from the file {file_path}.")
    except Exception as e:
        print(f"An error occurred: {e}")

def is_package_info_valid( packageInfo: dict ):
    
    if not isinstance(packageInfo, dict):
        return False

    if( list( packageInfo.keys() ) == [] ):
        return False
    
    if packageInfo.get("dependencies") is None:
        return False
    
    if packageInfo.get("devDependencies") is None:
        return False
    
    return True

def get_dependencies( packageInfo: dict ):
    
    if not is_package_info_valid(packageInfo):
        raise MessageError("Package information is not valid. Please check the packages.json file content")
    
    dependencies = {
     "devDependencies": [],
     "dependencies": [],   
    }

    try:
      dependencies['dependencies'] = list( packageInfo.get("dependencies").keys() )
      dependencies['devDependencies'] = list( packageInfo.get("devDependencies").keys() )

    except Exception:
        raise MessageError("Some Error happen while is gathering dependencies information")

    return dependencies

def string_list_to_string( stringList: list ):
    return " ".join( stringList )

def get_argument_parser_action():
    # Create ArgumentParser object
    parser = argparse.ArgumentParser(description='Packages Management')

    # Add positional arguments
    parser.add_argument('arg1', type=str, help='Action Update')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Accessing parsed arguments
    return args.arg1

def update_packages( file_path: str ):

    clear_console()
    print(f'JSON File to Read {file_path}')
    # Step 1 - Read package.json file and Getting Dependencies
    dependencies = get_dependencies( read_package_file( file_path ) )

    # Step 2 - Delete node_modules folder
    remove_node_modules_folder()

    # Step 3 - Use command -> yarn remove to remove dependencies
    execute_command(['powershell', '-Command', 'yarn', 'remove', string_list_to_string( dependencies['dependencies'] )])
    execute_command(['powershell', '-Command', 'yarn', 'remove', string_list_to_string( dependencies['devDependencies'] )])

    # Step 4 - Delete Yarn.lock file
    remove_yarn_lock_file()

    # Step 5 - Re-Install Dependencies
    execute_command(['powershell', '-Command', 'yarn', 'add', string_list_to_string( dependencies['dependencies'] )])
    execute_command(['powershell', '-Command', 'yarn', 'add', '-D', string_list_to_string( dependencies['devDependencies'] )])

