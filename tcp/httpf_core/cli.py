from argparse import ArgumentParser

class Cli:

    @staticmethod
    def create_parser():
        # create the main parser for CLI
        main_parser = ArgumentParser(prog='httpf_core',
                                     description='httpc_core is a simple file server.',
                                     add_help=False,
                                     conflict_handler='resolve')
        # create a general template for GET and POST
        main_parser.add_argument('-v',
                                 dest='verbose',
                                 action='store_const',
                                 const=True,
                                 default=False,
                                 help='Print debugging messages.')
        main_parser.add_argument('-p',
                                 dest='port',
                                 action='store',
                                 default='8080',
                                 help='Specifies the port number that the server will listen and serve at. Default is 8080')
        main_parser.add_argument('-d',
                                 dest='directory',
                                 action='store',
                                 default='file/',
                                 help='Specifies the directory that the server will use to read/write requested files. Default is the current directory when launching the application.')
        return main_parser




