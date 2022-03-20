import sys
from argparse import ArgumentParser

from fog_nodes_manager import ManagerFogNodes
from variables import POOL_PORT,POOL_ROOT_IP,POOL_FN_PORT,POOL_CM_PORT,PORT_DISPATCHER_CLIENTS_MANAGER
from PyQt5.QtWidgets import QApplication
from command_parser import CommandParser
from app_client import AppClient
from clients_manager import DispatcherClientsManager
from pool import Pool

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-c', '--console', default=False, type=bool,
                        help='run application in console')
    args = parser.parse_args()
    if args.console:
        parser = CommandParser()
        parser.add_command('create_pool')
        parser.add_argument('create_pool', '--port_pool', default=POOL_PORT)
        parser.add_argument('create_pool', '--port_cm', default=POOL_CM_PORT)
        parser.add_argument('create_pool', '--port_fn', default=POOL_FN_PORT)

        parser.add_command('add_fog_node')

        mfn = ManagerFogNodes()
        mfn.load_fog_nodes('data/fog_nodes/key')
        while True:

            result = parser.parse_string(input())
            if result:
                if result[0] == 'create_pool':
                    port_pool, port_cm, port_fn = result[1]
                    pool = Pool(port_pool=port_pool, port_cm=port_cm, port_fn=port_fn)
                    pool.start()
                if result[0] == 'add_fog_node':
                    mfn.add_fog_node()
            else:
                print('Неизвестная команда')

    else:
        app = QApplication(sys.argv)
        dispatcher = DispatcherClientsManager(PORT_DISPATCHER_CLIENTS_MANAGER)
        dispatcher.start()

        client_manager = AppClient()
        client_manager.show()
        sys.exit(app.exec_())
# create_pool --port_pool 2323 --port_cm 2324 --port_fn 2325
# decloud.py -c True