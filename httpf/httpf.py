from httpf.cli import Cli
from httpf.api import Api
import os


if __name__ == '__main__':

    args = Cli.create_parser().parse_args()
    print(args)
    if not os.path.isdir(args.directory):
        os.mkdir(args.directory)
    with open(args.directory + '/hey.txt', 'w+') as f:
        f.write('1')
    api = Api()
    api.httpfs(int(args.port), args.verbose)
