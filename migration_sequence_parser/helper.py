import os
import sys
import importlib.util as util


def get_file_name_from_path(path_to_file):
    file_name = path_to_file[path_to_file.rfind("\\") + 1:]
    return file_name

def get_module_from_file_path(module_name, file_path):
    try:
        spec = util.spec_from_file_location(module_name, file_path)
        module = util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except ModuleNotFoundError:
        error_message = str(sys.exc_info()[1])
        missing_module = error_message[error_message.find('\''):]
        sys.tracebacklimit = 0
        raise Exception(f"{error_message}\nEnsure {missing_module} module is present in requirements.txt and installed properly")

def get_revision_id(file_name, module):
    try:
        return module.revision
    except AttributeError:
        # print(f'{file_name} is not a valid migration file')
        return "Not a revision file"

def get_down_revision(file_name, module):
    try:
        return module.down_revision
    except AttributeError:
        # print(f'Cannot determine position of {file_name}')
        return "Cannot find down_revision"

def get_files_from_folder(path_to_folder):
    file_paths = [
        item.path 
        for item in os.scandir(path_to_folder) 
        if os.path.isfile(item.path)
        ]

    return file_paths

def generate_migration_nodes(file_paths):
    nodes = {
        MigrationNode(file_path).revision_id
        :
        MigrationNode(file_path)
        for file_path in file_paths
    }
    
    return nodes

def get_head_nodes(nodes):
    head_nodes = [
        node 
        for node in nodes.values() 
        if node.is_head()
        ]
    return head_nodes

def validate_head(heads):
    if len(heads) > 1:
        head_files = ""
        for head in heads:
            head_files = head_files + "\n        " + head.file_name
        sys.tracebacklimit = 0
        raise Exception(f'Cannot determine first migration script...\n\n\
        Multiple head migration nodes exist in the package, check the files below...\n\
        **************************************************************************************\
        {head_files}\n\
        **************************************************************************************')
    return

def link_nodes(nodes):
    for node in nodes.values():
        try:
            if nodes[node.down_revision].next != None:
                sys.tracebacklimit = 0
                raise Exception(f'{nodes[node.down_revision].file_name} has more than 1 downstream files...\n\n\
            check the files below...\n\n\
            **************************************************************************************\n\
            {node.file_name}\n\
            {nodes[node.down_revision].next.file_name}\n\
            **************************************************************************************')
            nodes[node.down_revision].next = node
        except KeyError:
            if node.down_revision == None:
                pass

    heads = get_head_nodes(nodes)
    print('determining first migration file...')
    validate_head(heads)

    head = None
    try:
        head = heads[0]
    except IndexError:
        sys.tracebacklimit = 0
        raise Exception("Unable to link nodes, cannot determine first migration file")

    return head

def validate_nodes(nodes):
    invalid_nodes = []
    for node in nodes.values():
        if node.is_head():
            pass
        else:
            try:
                nodes[node.down_revision]
            except KeyError:
                invalid_nodes.append(node.file_name)
    if len(invalid_nodes) != 0:
        print('Cannot determine position of the following files')
        print("**************************************************************************************")
        for file_name in invalid_nodes:
            print(f'{file_name}\n')
        print("**************************************************************************************")

class MigrationNode:
    def __init__(self, file_path) -> None:
        self.file_path = file_path
        self.file_name = get_file_name_from_path(file_path)
        self.module = get_module_from_file_path('temp_module', file_path)
        self.revision_id = get_revision_id(self.file_name, self.module)
        self.down_revision = get_down_revision(self.file_name, self.module)
        self.next = None

    def is_head(self):
        return self.down_revision == None

    def migrate(self):
        if self.next == None:
            return str(self)
        return str(self) + " -> " + str(self.next.migrate())
    
    def __str__(self) -> str:
        return f'{self.revision_id}({self.file_name})'