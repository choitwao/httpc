from httpf_core.cli import Cli
from httpf_core.server import Server
import os


if __name__ == '__main__':

    args = Cli.create_parser().parse_args()
    s = Server(int(args.port), args.verbose, args.directory)
    s.run()
