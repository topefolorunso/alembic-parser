import time

def execute(node):
    file_name = node.file_name
    print (f"executing migration file {file_name}")
    time.sleep(3)
    if (node.next != None):
        execute(node.next)
    else:
        print (f"Migration successfully completed")

def confirm_execution():
    user_input = input("Proceed with sequence execution?\n(Y/n): ")
    if user_input.lower() == "y":
        return True
    return False