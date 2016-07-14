__author__ = 'liming'


from flask.ext.restful import reqparse
import optparse


def get_parser(arguments):
    parser = reqparse.RequestParser()
    for arg in arguments:
        parser.add_argument(arg)
    return parser

def get_options():
    parser = optparse.OptionParser()

    parser.add_option('-c', '--cfg',
                      action='store',
                      help='Path of config file')

    parser.add_option('-D', '--daemon',
                      action='store_true',
                      default=False,
                      help='run in background')

    options, _ = parser.parse_args()
    return parser, options