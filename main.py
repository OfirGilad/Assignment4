from Repository import _Repository
import os
import sys


def main(args):
    db_path = 'database.db'
    is_database_exist = os.path.isfile(db_path)
    config = args[1]
    orders = args[2]
    output = args[3]
    repo = _Repository(db_path)
    if not is_database_exist:
        repo.create_tables()
        repo.config_decode(config)
        repo.print_all()
    repo.execute_orders(orders, output)
    repo.close()


if __name__ == '__main__':
    main(sys.argv)
