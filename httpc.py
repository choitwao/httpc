from cli import Cli
from request import Request
import os


if __name__ == '__main__':

    args = Cli.create_parser().parse_args()
    request = Request()
    if args.subparser_name.upper() == 'GET':
        response = request.get(args.URL, args.headers)
    else:
        if args.file is not None and args.data is not None:
            print('You are not allowed to have -d and -f at the same time.')
            os._exit(1)
        if args.file is not None:
            with open(args.file, mode="r") as f:
                data = f.read()
        elif args.data is not None:
            data = args.data
        else:
            data = ''
        response = request.post(args.URL, args.headers, data)
    if args.verbose:
        print(response)
