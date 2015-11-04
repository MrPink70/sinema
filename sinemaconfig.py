__author__ = 'fabrizio rosa'

import ConfigParser
import os.path


class SinemaConfig:
    defdate = '200101010000'

    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        if os.path.isfile("test.cfg"):
            self.config.readfp(open('test.cfg'))

    def _save_config(self):
        with open('test.cfg', 'w') as conffile:
            self.config.write(conffile)

    def add_system(self, system):
        if self.config.has_section(system):
            print 'ERROR: System already exists: {Sys:s}'.format(**{"Sys": system})
            exit()
        self.config.add_section(system)
        self._save_config()

    def add_function(self,
                     system,
                     room,
                     node,
                     user,
                     function,
                     value=defdate):
        sep = '.'
        func_id_fields = (room, node, user, function)
        option = sep.join(func_id_fields)
        if not self.config.has_section(system):
            self.config.add_section(system)
        if self.config.has_option(system, option):
            print 'ERROR: Function already exists: {Opt:s}'.format(**{"Opt": option})
            exit()
        self.config.set(system, option, value)
        self._save_config()

    def upd_function(self,
                     system,
                     room,
                     node,
                     user,
                     function,
                     value):
        sep = '.'
        func_id_fields = (room, node, user, function)
        option = sep.join(func_id_fields)
        if not self.config.has_option(system, option):
            print 'ERROR: Function does not exists: {Opt:s}'.format(**{"Opt": option})
            exit()
        self.config.set(system, option, value)
        self._save_config()

    def rst_function(self,
                     system,
                     room,
                     node,
                     user,
                     function):
        sep = '.'
        func_id_fields = (room, node, user, function)
        option = sep.join(func_id_fields)
        if not self.config.has_option(system, option):
            print 'ERROR: Function does not exists: {Opt:s}'.format(**{"Opt": option})
            exit()
        self.config.set(system, option, self.defdate)
        self._save_config()

    def list_sections(self):
        syslist = self.config.sections()
        if len(syslist) > 0:
            for s in syslist:
                print s
        else:
            print "INFO: No system configured"

    def list_system_functions(self,
                              system):
        if not self.config.has_section(system):
            print 'ERROR: System does not exists: {Sys:s}'.format(**{"Sys": system})
            exit()
        funlist = self.config.items(system)
        sep = '.'
        room = None
        node = None
        user = None
        if len(funlist) > 0:
            for (fun, val) in funlist:
                (r, n, u, f,) = fun.split(sep)
                if not r == room:
                    print 'Room: {Room:s}'.format(**{"Room": r})
                    room = r
                if not n == node:
                    print '  Node: {Node:s}'.format(**{"Node": n})
                    node = n
                if not u == user:
                    print '    User: {User:s}'.format(**{"User": u})
                    user = u
                data = '      {FunctionName:12s} Updated: {Value:13s}'.format(**{"FunctionName": f, "Value": val})
                print data
        else:
            print 'INFO: no function configured for system {Sys:s}'.format(**{"Sys": system})

    def list_system_rooms(self,
                          system):
        if not self.config.has_section(system):
            print 'ERROR: System does not exists: {Sys:s}'.format(**{"Sys": system})
            exit()
        sep = '.'
        rooms = list()
        for (fun, val) in self.config.items(system):
            (r, n, u, f) = fun.split(sep)
            if r not in rooms:
                rooms.append(r)
        if len(rooms) > 0:
            for r in rooms:
                print r
        else:
            print 'INFO: no room configured for system {Sys:s}'.format(**{"Sys": system})

    def list_system_room_nodes(self,
                               system,
                               room):
        if not self.config.has_section(system):
            print 'ERROR: System does not exists: {Sys:s}'.format(**{"Sys": system})
            exit()
        sep = '.'
        roomfound = False
        nodes = list()
        for (fun, val) in self.config.items(system):
            (r, n, u, f) = fun.split(sep)
            if r == room:
                roomfound = True
                if n not in nodes:
                    nodes.append(n)
        if roomfound:
            if len(nodes) > 0:
                for n in nodes:
                    print n
            else:
                print 'INFO: no node configured for room {Room:s} in system {Sys:s}'.format(
                    **{"Room": room, "Sys": system})
        else:
            print 'ERROR: there is no room {Room:s} in system {Sys:s}'.format(**{"Room": room, "Sys": system})


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
    c = args.command
    s = args.system
    r = args.room
    n = args.node
    u = args.user
    f = args.function
    v = args.value
    mode = -1
    if s and r and n and u and f and v:
        mode = 6
    elif s and r and n and u and f and not v:
        mode = 5
    elif s and r and n and u and not f and not v:
        mode = 4
    elif s and r and n and not u and not f and not v:
        mode = 3
    elif s and r and not n and not u and not f and not v:
        mode = 2
    elif s and not r and not n and not u and not f and not v:
        mode = 1
    elif not s and not r and not n and not u and not f and not v:
        mode = 0
    else:
        print 'ERROR: Wrong parameter sequence'

    if c == "add":
        if mode == 1:
            configuration.add_system(s)
        elif mode == 5:
            configuration.add_function(s, r, n, u, f)
        elif mode == 6:
            configuration.add_function(s, r, n, u, f, v)
        else:
            print 'ERROR: Missing parameter(s)'
    elif c == "upd":
        if mode == 6:
            configuration.upd_function(s, r, n, u, f, v)
        else:
            print 'ERROR: Missing parameter(s)'
    elif c == "del":
        print "INFO: order not implemented"
    elif c == "rst":
        if mode == 5:
            configuration.rst_function(s, r, n, u, f)
        else:
            print 'ERROR: Wrong parameter sequence'
    elif c == "list":
        if mode == 0:
            configuration.list_sections()
        elif mode == 1:
            configuration.list_system_rooms(s)
        elif mode == 2:
            if r == "all":
                configuration.list_system_functions(s)
            else:
                configuration.list_system_room_nodes(s, r)
        else:
            print "ERROR: too many parameters"
