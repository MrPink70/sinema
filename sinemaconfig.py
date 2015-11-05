__author__ = 'Fabrizio Rosa'

import ConfigParser
import os.path
from collections import OrderedDict

DEFAULT_DATE = '200101010000'
SEP = '.'


class SinemaConfig:

    def __init__(self):
        self.config = ConfigParser.ConfigParser(dict_type=OrderedDict)
        if os.path.isfile("test.cfg"):
            self.config.readfp(open('test.cfg'))

    def _save_config(self):
        with open('test.cfg', 'w') as configuration_file:
            self.config.write(configuration_file)

    def _search_options(self, system='all', room='all', node='all', user='all', function='all'):
        reply = list()
        if system == 'all':
            systems_list = self.config.sections()
        else:
            systems_list = [system]
        for s in systems_list:
            functions_list = self.config.options(s)
            for option in functions_list:
                (r, n, u, f) = option.split(SEP)
                if room == 'all' or room == r:
                    if node == 'all' or node == n:
                        if user == 'all' or user == u:
                            if function == 'all' or function == f:
                                reply.append(option)
        return reply

    def _del_options(self, system, option_list):
        for option in option_list:
            self.config.remove_option(system, option)
        self._save_config()

    def add_system(self, system):
        if self.config.has_section(system):
            print 'ERROR: System already exists: {Sys:s}'.format(**{
                "Sys": system
            })
            exit()
        self.config.add_section(system)
        self._save_config()

    def add_function(self, system, room, node, user, function, value=DEFAULT_DATE):
        func_id_fields = (room, node, user, function)
        option = SEP.join(func_id_fields)
        if not self.config.has_section(system):
            self.config.add_section(system)
        if self.config.has_option(system, option):
            print 'ERROR: Function already exists: {Opt:s}'.format(**{
                "Opt": option
            })
            exit()
        self.config.set(system, option, value)
        self._save_config()

    def upd_function(self, system, room, node, user, function, value):
        func_id_fields = (room, node, user, function)
        option = SEP.join(func_id_fields)
        if not self.config.has_option(system, option):
            print 'ERROR: Function does not exists: {Opt:s}'.format(**{
                "Opt": option
            })
            exit()
        self.config.set(system, option, value)
        self._save_config()

    def rst_function(self, system, room, node, user, function):
        func_id_fields = (room, node, user, function)
        option = SEP.join(func_id_fields)
        if not self.config.has_option(system, option):
            print 'ERROR: Function does not exists: {Opt:s}'.format(**{
                "Opt": option
            })
            exit()
        self.config.set(system, option, DEFAULT_DATE)
        self._save_config()

    def del_function(self, system, room, node, user, function):
        functions_list = self._search_options(system, room, node, user, function)
        if len(functions_list) > 0:
            self._del_options(system, functions_list)
        else:
            print 'ERROR: Function {Func:s} does not exists on node {Node:s} for user {User:s}'.format(**{
                "Func": function,
                "Node": node,
                "User": user
            })

    def del_user(self, system, room, node, user):
        functions_list = self._search_options(system, room, node, user)
        if len(functions_list) > 0:
            self._del_options(system, functions_list)
        else:
            print 'ERROR: Room {Room:s} has no user {User:s} on node {Node:s}'.format(**{
                "Room": room,
                "User": user,
                "Node": node
            })

    def del_node(self, system, room, node):
        functions_list = self._search_options(system, room, node)
        if len(functions_list) > 0:
            self._del_options(system, functions_list)
        else:
            print 'ERROR: Room {Room:s} has no node {Node:s}'.format(**{
                "Room": room,
                "Node": node
            })

    def del_room(self, system, room):
        functions_list = self._search_options(system, room)
        if len(functions_list) > 0:
            self._del_options(system, functions_list)
        else:
            print 'ERROR: Room {Room:s} does not exists'.format(**{
                "Room": room
            })

    def del_system(self, system):
        if self.config.has_section(system):
            self.config.remove_section(sys)
            self._save_config()
        else:
            print 'ERROR: System {Sys:s} not present in configuration'.format(**{
                "Sys": system
            })

    def list_sections(self):
        systems_list = self.config.sections()
        if len(systems_list) > 0:
            for s in systems_list:
                print s
        else:
            print "INFO: No system configured"

    def list_system_functions(self, system):
        if not self.config.has_section(system):
            print 'ERROR: System does not exists: {Sys:s}'.format(**{
                "Sys": system
            })
            exit()
        functions_list = self.config.items(system)
        room = None
        node = None
        user = None
        if len(functions_list) > 0:
            for (fun, val) in functions_list:
                (r, n, u, f,) = fun.split(SEP)
                if not r == room:
                    print 'Room: {Room:s}'.format(**{
                        "Room": r
                    })
                    room = r
                if not n == node:
                    print '  Node: {Node:s}'.format(**{
                        "Node": n
                    })
                    node = n
                if not u == user:
                    print '    User: {User:s}'.format(**{
                        "User": u
                    })
                    user = u
                data = '      {FunctionName:12s} Updated: {Value:13s}'.format(**{
                    "FunctionName": f,
                    "Value": val
                })
                print data
        else:
            print 'INFO: no function configured for system {Sys:s}'.format(**{
                "Sys": system
            })

    def list_system_rooms(self, system):
        if not self.config.has_section(system):
            print 'ERROR: System does not exists: {Sys:s}'.format(**{
                "Sys": system
            })
            exit()
        rooms = list()
        for (fun, val) in self.config.items(system):
            (r, n, u, f) = fun.split(SEP)
            if r not in rooms:
                rooms.append(r)
        if len(rooms) > 0:
            for r in rooms:
                print r
        else:
            print 'INFO: no room configured for system {Sys:s}'.format(**{
                "Sys": system
            })

    def list_system_room_nodes(self, system, room):
        if not self.config.has_section(system):
            print 'ERROR: System does not exists: {Sys:s}'.format(**{
                "Sys": system
            })
            exit()
        room_found = False
        nodes = list()
        for (fun, val) in self.config.items(system):
            (r, n, u, f) = fun.split(SEP)
            if r == room:
                room_found = True
                if n not in nodes:
                    nodes.append(n)
        if room_found:
            if len(nodes) > 0:
                for n in nodes:
                    print n
            else:
                print 'INFO: no node configured for room {Room:s} in system {Sys:s}'.format(**{
                    "Room": room,
                    "Sys": system
                })
        else:
            print 'ERROR: there is no room {Room:s} in system {Sys:s}'.format(**{
                "Room": room,
                "Sys": system
            })


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Manipulate configuration file')
    parser.add_argument("command",
                        metavar="CMD",
                        choices=['add', 'upd', 'del', 'rst', 'list'],
                        help="the command to execute on the configuration"
                        )
    parser.add_argument("system",
                        metavar="SYS",
                        nargs='?',
                        default=None,
                        help="the system name"
                        )
    parser.add_argument("room",
                        metavar="ROOM",
                        nargs='?',
                        default=None,
                        help="the room of the node in the system SYS"
                        )
    parser.add_argument("node",
                        metavar="NODE",
                        nargs='?',
                        default=None,
                        help="the node name"
                        )
    parser.add_argument("user",
                        metavar="USER",
                        nargs='?',
                        default=None,
                        help="the username to use to connect to the node NODE"
                        )
    parser.add_argument("function",
                        metavar="FUNC",
                        nargs='?',
                        default=None,
                        help="the function name"
                        )
    parser.add_argument("value",
                        metavar="VAL",
                        nargs='?',
                        default=None,
                        help="the value for the function (valid only for update and add function"
                        )

    args = parser.parse_args()
    configuration = SinemaConfig()
    missing_error = 'ERROR: {Object:s} is missing'
    cmd = args.command
    sys = args.system
    roo = args.room
    nod = args.node
    usr = args.user
    fnc = args.function
    vle = args.value
    mode = -1
    if sys and roo and nod and usr and fnc and vle:
        mode = 6
    elif sys and roo and nod and usr and fnc and not vle:
        mode = 5
    elif sys and roo and nod and usr and not fnc and not vle:
        mode = 4
    elif sys and roo and nod and not usr and not fnc and not vle:
        mode = 3
    elif sys and roo and not nod and not usr and not fnc and not vle:
        mode = 2
    elif sys and not roo and not nod and not usr and not fnc and not vle:
        mode = 1
    elif not sys and not roo and not nod and not usr and not fnc and not vle:
        mode = 0
    else:
        print 'ERROR: Wrong parameter sequence'

    if cmd == "add":
        if mode == 1:
            configuration.add_system(sys)
        elif mode == 5:
            configuration.add_function(sys, roo, nod, usr, fnc)
        elif mode == 6:
            configuration.add_function(sys, roo, nod, usr, fnc, vle)
        else:
            print 'ERROR: Missing parameter(s)'
    elif cmd == "upd":
        if mode == 6:
            configuration.upd_function(sys, roo, nod, usr, fnc, vle)
        else:
            print 'ERROR: Missing parameter(s)'
    elif cmd == "del":
        if mode == 5:
            configuration.del_function(sys, roo, nod, usr, fnc)
        elif mode == 4:
            configuration.del_user(sys, roo, nod, usr)
        elif mode == 3:
            configuration.del_node(sys, roo, nod)
        elif mode == 2:
            configuration.del_room(sys, roo)
        elif mode == 1:
            configuration.del_system(sys)
        else:
            print 'ERROR: Wrong parameter sequence'
    elif cmd == "rst":
        if mode == 5:
            configuration.rst_function(sys, roo, nod, usr, fnc)
        else:
            print 'ERROR: Wrong parameter sequence'
    elif cmd == "list":
        if mode == 0:
            configuration.list_sections()
        elif mode == 1:
            configuration.list_system_rooms(sys)
        elif mode == 2:
            if roo == "all":
                configuration.list_system_functions(sys)
            else:
                configuration.list_system_room_nodes(sys, roo)
        else:
            print "ERROR: too many parameters"
