
class FileNode:
    def __init__(self, file_path) -> None:
        self.file_path = file_path
        self.file_name = self.get_file_name()
        self.module_name = self.file_name[:-3]

        import importlib.util as util
        self.module = self.get_module_from_file_path(self.module_name, self.file_path, util)

        self.revision_id = self.get_revision_id()
        self.down_revision = self.get_down_revision()
        self.next = None        


    def get_file_name(self):
        file_name = self.file_path[self.file_path.rfind("\\") + 1:]
        return file_name

    def get_revision_id(self):
        try:
            return self.module.revision
        except AttributeError:
            return "Not a revision file"

    def get_down_revision(self):
        try:
            return self.module.down_revision
        except AttributeError:
            return "Not a revision file"

    def is_head(self):
        return self.down_revision == None
    
    def __str__(self) -> str:
        return f'{self.revision_id}({self.file_name})'


    def get_module_from_file_path(self, module_name, file_path, util):
        try:
            spec = util.spec_from_file_location(module_name, file_path)
            module = util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        except:
            return


class LinkedFiles:
    def __init__(self, root_dir) -> None:
        self.root_dir = root_dir
        self.fileNodes = self.get_file_nodes()
        self.heads = self.get_heads()

    def get_file_nodes(self):
        from os import walk
        from os.path import join

        dir_path = self.root_dir
        file_paths = []
        for (dir_path, dir_names, file_names) in walk(dir_path):
            paths = [join(dir_path, file_name) for file_name in file_names if file_name[-2:] == 'py']
            file_paths.extend(paths)

        file_nodes = {
            FileNode(file_path).revision_id
            :
            FileNode(file_path)
            for file_path in file_paths
        }
        
        return file_nodes
    
    def get_heads(self):
        return [fileNode for fileNode in self.fileNodes.values() if fileNode.is_head()]

    def link_files(self):
        for file in self.fileNodes.values():
            try:
                self.fileNodes[file.down_revision].next = file
            except KeyError:
                pass
        return

    def __str__(self) -> str:
        links = ""
        for head in self.heads:
            link = str(head)
            while head.next != None:
                head = head.next
                link = link + ' -> ' + str(head)
            links = links + link + '\n'
        return links