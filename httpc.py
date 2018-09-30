from parser import Parser


if __name__ == '__main__':

    # Parsing user command
    parser = Parser.create_parser()
    command = parser.parse_args()

