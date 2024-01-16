import sys
import argparse

from script_files.user_actions import UserAction


info = '''
    Script coded by Wojciech Piwowarski

    LIST OF ALL COMMANDS:
    ## Create Database file, no auth need:

        create_database

    
    ## Commands for admin only:

        print-all-accounts --login <login> --password <password>
        print-oldest-account --login <login> --password <password>
        group-by-age --login <login> --password <password>

    
    ## Commands for all users:

        print-children --login <login> --password <password>
        find-similar-children-by-age --login <login> --password <password>
    '''


class CustomArgumentParser(argparse.ArgumentParser):
    """
    Custom class for return custom messages
    """

    def error(self, message):
        """
        Error handling rewrited message
        """
       
        message = 'Wrong command type -h for Help'
        self.print_usage()
        self.exit(2, f"{message}\n")

    def format_help(self):
        """
        Rewrited help message
        """
        return  info
        

def commander():
    """
    Main function for managing behavior of script, \n
    Designed and coded by Wojciech Piwowarski     \n
    as recrutation task to intern in   \n
    Profil-Software company    \n
    """

    c_prog = 'CLI Python Scipt'
    c_description = 'Sript, for collecting data, from CSV, XML, JSON files'

    parser = CustomArgumentParser(
        prog = c_prog,
        usage = info,
        description = c_description,
        add_help = True,
        )
    
    subparsers = parser.add_subparsers(
        dest='command', metavar='''  Command list''', help='''   Description''')
    
    #
    # Command name  (Without authentication)
    # scripy.py create_database
    #        
    create_database = subparsers.add_parser(
        'create_database', help='Create Database')
    
    #
    # Command Name   (For admins only)
    # script.py print-all-accounts --login <login> --password <password>
    #
    print_all_accounts = subparsers.add_parser(
        'print-all-accounts', help='Print all accounts')
    
    print_all_accounts.add_argument(
        '--login', required='print-all-accounts' in sys.argv, help='Login')
    
    print_all_accounts.add_argument(
        '--password', required='print-all-accounts' in sys.argv, help='Password')

    #
    # Command Name   (For admins only)
    # script.py print-oldest-account --login <login> --password <password>
    #
    print_oldest_account = subparsers.add_parser(
        'print-oldest-account', help='Print oldest account')
    
    print_oldest_account.add_argument(
        '--login', required='print-oldest-account' in sys.argv, help='Login')
    
    print_oldest_account.add_argument(
        '--password', required='print-oldest-account' in sys.argv, help='Password')

    #
    # Command Name   (For admins only)
    # script.py group-by-age --login <login> --password <password>
    #
    group_by_age = subparsers.add_parser(
        'group-by-age', help='Group by age')
    
    group_by_age.add_argument(
        '--login', required='group-by-age' in sys.argv, help='Login')
    
    group_by_age.add_argument(
        '--password', required='group-by-age' in sys.argv, help='Password')
    
    #
    # Command Name   (For all users)
    # script.py print-children --login <login> --password <password>
    # 
    print_children = subparsers.add_parser(
        'print-children', help='Print children')
    
    print_children.add_argument(
        '--login', required='print-children' in sys.argv, help='Login')
    
    print_children.add_argument(
        '--password', required='print-children' in sys.argv, help='Password')

    #
    # Command Name   (For all users)
    # script.py find-similar-children-by-age --login <login> --password <password>
    #
    similar_children = subparsers.add_parser(
        'find-similar-children-by-age', help='Find similar children by age')
    
    similar_children.add_argument(
        '--login', required='find-similar-children-by-age' in sys.argv, help='Login')
    
    similar_children.add_argument(
        '--password', required='find-similar-children-by-age' in sys.argv, help='Password')
    
    #
    #
    similar_children = subparsers.add_parser(
        'secret-command', help='')
    
    similar_children.add_argument(
        '--login', required='secret-command' in sys.argv, help='')
    
    similar_children.add_argument(
        '--password', required='secret-command' in sys.argv, help='')
    
    args = parser.parse_args()


    #
    # No auth
    if args.command == 'create_database':    
        status = UserAction.func_create_database()
        print(status)

    # For admin 
    elif args.command == 'print-all-accounts':  
        result = UserAction.func_print_all_accounts(args.login, args.password)
        print(result)

    # For admin
    elif args.command == 'print-oldest-account':  
        result = UserAction.func_print_oldest_account(args.login, args.password)
        print(result)

    # For admin    
    elif args.command == 'group-by-age':      
        result = UserAction.func_group_by_age(args.login, args.password)
        print(result)

    # For User
    elif args.command == 'print-children':    
        result = UserAction.func_print_children(args.login, args.password)
        print(result)

    # For User
    elif args.command == 'find-similar-children-by-age':  
        result = UserAction.func_find_similar_children(args.login, args.password)
        print(result)

    # For those who knows ;)
    elif args.command == 'secret-command':  
        result = UserAction.func_secret_command(args.login, args.password)
        print(result)


        
# Initiation of main function commander()
if __name__ == '__main__':
    commander()


