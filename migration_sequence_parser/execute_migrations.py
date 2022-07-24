import time


def execute(node, executed_nodes):
    print (f"executing migration file {node.file_name}")
    executed_nodes.append(node)
    try:
        node.module.upgrade()
    except NameError:
        pass
    except:
        raise Exception(f'{node.file_name}')
    time.sleep(3)
    if (node.next != None):
        execute(node.next, executed_nodes)
    else:
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
        try:
            node.module.downgrade()
        except NameError:
            pass
        time.sleep(3)
    print("roll back successfull")