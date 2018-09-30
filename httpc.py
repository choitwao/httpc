from argparse import ArgumentParser


class Httpc:

    def __init__(self, verb, header, inline_data, file):
        self.verb = verb
        self.header = header
        self.inline_data = inline_data
        self.file = file


    def argParser(self):
        # 1 Create the main parser
        mainParser = ArgumentParser(prog='httpc',
                                    description="httpc is a curl-like application but supports HTTP protocol only",
                                    add_help=False,
                                    conflict_handler='resolve')
        # 1.1 Add verbose option
        mainParser.add_argument('-v',
                                dest="isVerbose",
                                action="store_const",
                                const=True,
                                default=False,
                                help="Prints the detail of the response such as protocol, status, and headers.")
        # 1.2 Add header option
        mainParser.add_argument('-h',
                                dest="headers",
                                action="append",
                                metavar="key:value",
                                help="Associates headers to HTTP Request with the format 'key:value'")
        # 1.3 Add URL option
        mainParser.add_argument('URL',
                                action="store",
                                help="URL for the Http request")
        # 1.4 Add sub-parsers for methods
        sub_parser = mainParser.add_subparsers(help='[command] help', dest="subparser_name")
        sub_parser.required = True

        # 2 GET sub-parser
        getParser = sub_parser.add_parser('get',
                                          parents=[mainParser],
                                          help='Get executes a HTTP GET request for a given URL.')

        # 3 POST sub-parser
        postParser = sub_parser.add_parser('post',
                                           parents=[mainParser],
                                           epilog="Either [-d] or [-f] can be used but not both.",
                                           help='Post executes a HTTP POST request for a given URL with inline data or from file.')
        postParser.add_argument('-d', dest="data", action="store",
                                metavar="inline-data",
                                help="Associates an inline data to the body HTTP POST")
        postParser.add_argument('-f', dest="file", action="store",
                                metavar="file",
                                help="Associates an inline data to the body HTTP POST")
        return mainParser
