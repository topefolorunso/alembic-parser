from helper import *
import os

if __name__ == "__main__":

    root_dir = os.getenv('root_dir')
    linked_files = LinkedFiles(root_dir)
    linked_files.link_files()
    print(linked_files)