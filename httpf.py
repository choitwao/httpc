from httpf_core.cli import Cli
from httpf_core.server import Server
import os


if __name__ == '__main__':

    args = Cli.create_parser().parse_args()
    print(args)
    if not os.path.isdir(args.directory):
        os.mkdir(args.directory)
    with open(args.directory + '/hey.txt', 'w+') as f:
        f.write('1')
    s = Server(int(args.port), args.verbose, args.directory)
    s.run()
