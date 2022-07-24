import time


def execute(node, executed_nodes):
    print (f"executing migration file {node.file_name}")
    time.sleep(3)
    executed_nodes.append(node)
    if (node.next != None):
        execute(node.next, executed_nodes)
    else:
        # raise Exception(f'{node.file_name}')
        print (f"Migration successfully completed")
    

def confirm_execution():
    user_input = input("Proceed with sequence execution?\n(Y/n): ")
    if user_input.lower() == "y":
        return True
    return False

def roll_back(executed_nodes):
    while len(executed_nodes) != 0:
        node = executed_nodes.pop()
        print(f"rolling back migration file {node.file_name}")
        time.sleep(3)
    print("roll back successfull")