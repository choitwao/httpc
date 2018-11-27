from tcp.httpf_core.cli import Cli
from tcp.httpf_core.server import Server

if __name__ == '__main__':

    args = Cli.create_parser().parse_args()
    s = Server(int(args.port), args.verbose, args.directory)
    s.run()
