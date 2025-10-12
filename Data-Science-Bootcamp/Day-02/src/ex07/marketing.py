import sys


def get_email_lists():
    """
    email list
    """
    clients = ['andrew@gmail.com', 'jessica@gmail.com', 'ted@mosby.com',
               'john@snow.is', 'bill_gates@live.com', 'mark@facebook.com',
               'elon@paypal.com', 'jessica@gmail.com']
    
    participants = ['walter@heisenberg.com', 'vasily@mail.ru',
                   'pinkman@yo.org', 'jessica@gmail.com', 'elon@paypal.com',
                   'pinkman@yo.org', 'mr@robot.gov', 'eleven@yahoo.com']
    
    recipients = ['andrew@gmail.com', 'jessica@gmail.com', 'john@snow.is']
    
    return clients, participants, recipients


def convert_to_sets():
    clients, participants, recipients = get_email_lists()
    
    clients_set = set(clients)
    participants_set = set(participants)
    recipients_set = set(recipients)
    
    return clients_set, participants_set, recipients_set


def call_center():
    clients_set, participants_set, recipients_set = convert_to_sets()
    
    call_center_list = clients_set - recipients_set
    
    return sorted(list(call_center_list))


def potential_clients():
    clients_set, participants_set, recipients_set = convert_to_sets()
    potential_clients_list = participants_set - clients_set
    
    return sorted(list(potential_clients_list))


def loyalty_program():
    clients_set, participants_set, recipients_set = convert_to_sets()
    loyalty_program_list = clients_set - participants_set
    
    return sorted(list(loyalty_program_list))


def execute_task(task_name):
    if task_name == 'call_center':
        return call_center()
    elif task_name == 'potential_clients':
        return potential_clients()
    elif task_name == 'loyalty_program':
        return loyalty_program()
    else:
        raise ValueError(f"Unknown task: {task_name}. Valid tasks are: call_center, potential_clients, loyalty_program")


def display_results(email_list):
    for email in email_list:
        print(email)


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 marketing.py <task_name>")
        print("Valid tasks: call_center, potential_clients, loyalty_program")
        return
    
    task_name = sys.argv[1]
    
    try:
        result = execute_task(task_name)
        display_results(result)
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()