#!/usr/bin/env python
#
# Copright (c) 2014, Nash E. Foster
#
#  This file is part of Exrpc.
#
#  Exrpc is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Exrpc is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Exrpc.  If not, see <http://www.gnu.org/licenses/>.
#
import argparse
import pkg_resources
import sys

import srv.string_service.StringService
from srv.string_service.ttypes import StringMessage
import thrift 

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer


def parse_args():
    """Parse command-line arguments."""
    prog_string = "echo.py"
    main = argparse.ArgumentParser(prog=prog_string)
    main.add_argument("--port", dest="port", default=1337, help="The TCP port.")
    main.add_argument("--debug", dest="debug", default=False,
            action="store_const", const=True, help="Enable debug output.")
    sub_parsers = main.add_subparsers(help="Avacloud sub-command help.")
    server = sub_parsers.add_parser("server")
    server.set_defaults(command="server")
    client = sub_parsers.add_parser("client")
    client.set_defaults(command="client")
    client.add_argument("strings", nargs="*", help="The strings to echo.")
    client.add_argument("--times", default=1, type=int,
            help="Number of times to echo.")
    return main.parse_args()


class StringServiceHandler(object):
    def echo(self, input_string):
        return input_string.content


def main():
    options = parse_args()
    if options.debug:
        print "Command: %s" % (options.command,)
    if options.command == "server":
        return server_main(options)

    if options.command == "client":
        return client_main(options)

    print "Invalid command. Try --help"

def client_main(options):
    if options.debug:
        print "client_main: go go gadget client!"
    sock = TSocket.TSocket('localhost', options.port)
    transport = TTransport.TBufferedTransport(sock)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = srv.string_service.StringService.Client(protocol)
    transport.open()
    original = " ".join(options.strings)
    msg = StringMessage(
            content=original,
            times=options.times)
    result = client.echo(msg)
    print "Original: %s\n    Echo: %s\n" % (original, result,)
    transport.close()
    return


def server_main(options):
    if options.debug:
        print "server_main: go go gadget server!"
    handler = StringServiceHandler()
    proc = srv.string_service.StringService.Processor(handler)
    xport = TSocket.TServerSocket(port=options.port)
    factory = TTransport.TBufferedTransportFactory()
    protofactory = TBinaryProtocol.TBinaryProtocolFactory()
    server = TServer.TThreadedServer(proc, xport, factory, protofactory)
    server.serve()
    return


if __name__ == '__main__':
    main()

