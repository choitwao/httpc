from argparse import ArgumentParser

class Cli:

    @staticmethod
    def create_parser():
        # create the main parser for CLI
        command_parser = ArgumentParser(prog="httpc_core",
                                        description="httpc_core is a curl-like application but supports HTTP protocol only")
        # create branches for GET and POST
        method_parsers = command_parser.add_subparsers(help='[command] help',
                                                       dest="subparser_name")
        method_parsers.required = True
        # create a general template for GET and POST
        template_parser = ArgumentParser(add_help=False,
                                         conflict_handler='resolve')
        template_parser.add_argument('-v',
                                     dest="verbose",
                                     action="store_const",
                                     const=True,
                                     default=False,
                                     help="Prints the detail of the response such as protocol, status, and headers.")
        template_parser.add_argument('-o',
                                     dest="output",
                                     action="store_const",
                                     const=True,
                                     default=False,
                                     help="Save the response in current directory")
        template_parser.add_argument('-H',
                                     dest="headers",
                                     action="append",
                                     metavar="key:value",
                                     help="Associates headers to HTTP Request with the format 'key:value'")
        template_parser.add_argument('URL',
                                     action="store",
                                     help="The URL address of your HTTP Request")
        # GET command
        get_parser = method_parsers.add_parser('get',
                                              parents=[template_parser],
                                              help='Get executes a HTTP GET request for a given URL.')

        # POST command
        post_parser = method_parsers.add_parser('post',
                                               parents=[template_parser],
                                               epilog="Either [-d] or [-f] can be used but not both.",
                                               help='Post executes a HTTP POST request for a given URL with inline data or from file.')
        post_parser.add_argument('--d',
                                dest="data",
                                action="store",
                                metavar="inline",
                                help="Associates an inline data to the body HTTP POST")
        post_parser.add_argument('-f',
                                dest="file",
                                action="store",
                                metavar="file",
                                help="Associates an inline data to the body HTTP POST")
        return command_parser




