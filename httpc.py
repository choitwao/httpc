from httpc_core.cli import Cli
from httpc_core.request import Request
import os


args = Cli.create_parser().parse_args()
request = Request()
if args.subparser_name.upper() == 'GET':
    response = request.get(args.URL, args.headers)
else:
    if args.file is not None and args.data is not None:
        print('You are not allowed to have -d and -f at the same time.')
        os._exit(1)
    if args.file is not None:
        data = ''
        with open(args.file, mode='r') as f:
            for line in f:
                if line:
                    data += line.rstrip('\n') + '&'
        if data[-1] == '&':
            parameters = data.rstrip('&')
    elif args.data is not None:
        data = args.data
    else:
        data = ''
    response = request.post(args.URL, args.headers, data)
if args.verbose:
    print(response)
if args.output:
    with open('httpc_core/output.txt', mode='w+') as w:
        w.write(response)
