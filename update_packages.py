from utils import *

clear_console()
# Step 1 - Read package.json file and Getting Dependencies
dependencies = get_dependencies( read_package_file() )

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



