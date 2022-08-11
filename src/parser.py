import os
import time
from helper import *
from execute_migrations import *

def get_migration_node(base_dir):
    file_paths = get_files_from_folder(base_dir)
    return generate_migration_nodes(file_paths)

def get_first_migration_scripts(nodes):
    print('validating nodes...')
    validate_nodes(nodes)
    print('linking migration nodes...')
    return link_nodes(nodes)

def generate_migration_sequence(head):
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

def commence_roll_back(message):
    print("**************************************************************************************")
    print(message)
    time.sleep(3)
    print("**************************************************************************************")
    roll_back(executed_nodes)

if __name__ == "__main__":
    base_dir = os.getenv('base_dir', r"..\test_data\migration_data_test")
    nodes = get_migration_node(base_dir)
    heads = get_first_migration_scripts(nodes)
    n=1
    for head in heads:
        print(f'generating migration sequence {n}...')
        generate_migration_sequence(head)
        n+=1

    for head in heads:
        executed_nodes = []
        try:
            run_execution(head, executed_nodes)
        except NameError:
            pass
        except KeyboardInterrupt:
            message = "Keyboard interrupt...\ncommencing roll back actions..."
            commence_roll_back(message)
        except:
            file_name = str(sys.exc_info()[1])
            message = f"Problem with migration file {file_name}...\ncommencing roll back actions..."
            commence_roll_back(message)
