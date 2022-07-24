import os
import time
from helper import *
from execute_migrations import *

def get_migration_node(base_dir):
    file_paths = get_files_from_folder(base_dir)
    return generate_migration_nodes(file_paths)

def get_first_migration_script(nodes):
    print('validating nodes...')
    validate_nodes(nodes)
    print('linking migration nodes...')
    return link_nodes(nodes)

def generate_migration_sequence(head):
    print('generating migration sequence...')
    print("**************************************************************************************")
    print("Migration files would be applied in below sequence\n")
    migration_sequence = head.migrate()
    print(migration_sequence)
    print("**************************************************************************************")

def run_execution(head, executed_nodes):
    if confirm_execution():
        execute(head, executed_nodes)
    else:
        print("sequence execution suppressed...")

def commence_roll_back():
    file_name = str(sys.exc_info()[1])
    print("**************************************************************************************")
    print(f"Problem with migration file {file_name}...\ncommencing roll back actions...")
    time.sleep(3)
    print("**************************************************************************************")
    roll_back(executed_nodes)

if __name__ == "__main__":
    base_dir = os.getenv('base_dir', r".\tests\migration_data_test")
    nodes = get_migration_node(base_dir)
    head = get_first_migration_script(nodes)
    generate_migration_sequence(head)

    executed_nodes = []
    # run_execution(head, executed_nodes)
    try:
        run_execution(head, executed_nodes)
    except NameError:
        pass
    except:
        commence_roll_back()
