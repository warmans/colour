__author__ = 'warmans'

import xml.etree.ElementTree as ET
import argparse
import sys
import re


class Formatter():

    def __init__(self, config_path):
        self.config_path = config_path

    def get_colour(self, name):
        colours = {
            'red': '\033[97;41m{0}\033[0m',
            'green': "\033[30;42m{0}\033[0m",
            'yellow': '\033[30;103m{0}\033[0m'
        }

        if name in colours.keys():
            return colours[name]
        else:
            return '{0}'

    #parse output
    def format(self, input_stream):

        #read config
        config = ET.parse(self.config_path)

        #parse input stream using config
        for line in input_stream:
            for line_style in config.getroot():

                formatted_line = ''
                matches = re.match(line_style.attrib['match'], line)

                if 'colour' in line_style.attrib.keys():
                    outer_colour = self.get_colour(line_style.attrib['colour'])
                else:
                    outer_colour = '{0}'

                if matches:
                    #if no sub-strings are defined output the whole line
                    if len(list(line_style)) > 0:
                        for substr in line_style:
                            match = int(substr.text)
                            colour = self.get_colour(substr.attrib['colour'])

                            #ignore full match - you shouldn't define substrings if you just want to output
                            #the full line
                            if match is not 0:
                                formatted_line = formatted_line + colour.format(matches.group(match))
                    else:
                        formatted_line = line.strip()

                    print outer_colour.format(formatted_line)


if __name__ == '__main__':

    #handle args
    parser = argparse.ArgumentParser()
    parser.add_argument("input", default=None, nargs='?')
    parser.add_argument("-c", "--cfg", nargs='?')
    args = parser.parse_args()

    #create formatter
    formatter = Formatter(args.cfg)

    # pipe
    if not sys.stdin.isatty():
        formatter.format(sys.stdin)

    # file
    else:
        input_filename = args.input

        if not input_filename:
            raise Exception('No pipe or file specified')

        with open(input_filename, 'rU') as input_stream:
            formatter.format(input_stream)