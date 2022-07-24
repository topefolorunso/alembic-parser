import os
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

if __name__ == "__main__":
    base_dir = os.getenv('base_dir', r".\migration_data_test")
    nodes = get_migration_node(base_dir)
    head = get_first_migration_script(nodes)
    generate_migration_sequence(head)

    if confirm_execution():
        execute(head)
    else:
        print("sequence execution suppressed...")
    