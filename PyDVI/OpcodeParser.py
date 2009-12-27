#####################################################################################################
#
# PyDVI - Python Library to Process DVI Stream
# Copyright (C) 2009 Salvaire Fabrice
#
#####################################################################################################

#####################################################################################################
#
# Audit
#
#  - 19/12/2009 fabrice
#
#####################################################################################################

#####################################################################################################

from Stream import *

#####################################################################################################

class OpcodeStreamParser(AbstractStream):
    
    ###############################################

    def __init__(self, opcode_definitions):

        '''
        Opcode Stream Parser
        '''

        self.__init_opcode_parsers(opcode_definitions)

    ###############################################

    def __init_opcode_parsers(self, opcode_definitions):

        '''
        opcode_definitions : (opcode_definition, ...)

        opcode_definition : 
          (opcode_indexes, opcode_name, opcode_description, opcode_parameters = (), opcode_class = None) |
          (opcode_indexes, opcode_parser_class),

        opcode_indexes :
          index |
          [lower_index, upper_index] # duplicate the opcode in the range

        opcode_parameters :
          (p0, p1, ...) |
          ([lower_n, upper_n]) # opcode at [index + i] has parameter p[i]
        '''

        # Allocate 256 opcode
        self.opcode_parsers = [None]*255

        for opcode_definition in opcode_definitions:
        
            # opcode index

            index = opcode_definition[0]
            
            if isinstance(index, list):
                lower_index = index[0]
                upper_index = index[1]
            else:
                lower_index = upper_index = index
        
            if isinstance(opcode_definition[1], str): # opcode description string
        
                name, description, parameters, opcode_class = opcode_definition[1:]
        
                if parameters is not None and isinstance(parameters, list):
                    lower_n, upper_n = parameters
                    if lower_n < 0:
                        signe = -1
                    else:
                        signe = 1
                    for n in xrange(abs(lower_n), abs(upper_n) +1):
                        i = index + n -1
                        self.opcode_parsers[i] = OpcodeParser(i, name, description, tuple([signe*n]), opcode_class)

                else:
                    for i in xrange(lower_index, upper_index +1):
                        self.opcode_parsers[i] = OpcodeParser(i, name, description, parameters, opcode_class)
        
            else: # OpcodeParser Class
                for i in xrange(lower_index, upper_index +1):
                    self.opcode_parsers[i] = opcode_definition[1](i)

        # for opcode_parser in self.opcode_parsers:
        #     print opcode_parser

#####################################################################################################

class OpcodeParser(object):

    ###############################################

    def __init__(self, opcode, name, description, parameters = (), opcode_class = None):

        '''
        Opcode Parser
        '''

        self.opcode = opcode
        self.name = name
        self.description = description
        self.opcode_class = opcode_class

        self.parameter_readers = []

        if parameters is not None and len(parameters) > 0:
            self.__init_parameter_readers__(parameters)

    ###############################################

    def __str__(self):

        return 'opcode %3u %s %s' % (self.opcode, self.name, self.description)

    ###############################################

    def __init_parameter_readers__(self, parameters):

        for parameter in parameters:
            if   parameter ==  1: parameter_reader = OpcodeStreamParser.read_unsigned_byte1
            elif parameter ==  2: parameter_reader = OpcodeStreamParser.read_unsigned_byte2
            elif parameter ==  3: parameter_reader = OpcodeStreamParser.read_unsigned_byte3
            elif parameter ==  4: parameter_reader = OpcodeStreamParser.read_unsigned_byte4
            elif parameter == -1: parameter_reader = OpcodeStreamParser.read_signed_byte1
            elif parameter == -2: parameter_reader = OpcodeStreamParser.read_signed_byte2
            elif parameter == -3: parameter_reader = OpcodeStreamParser.read_signed_byte3
            elif parameter == -4: parameter_reader = OpcodeStreamParser.read_signed_byte4
                
            self.parameter_readers.append(parameter_reader)

    ###############################################

    def read_parameters(self, opcode_parser):

        return map(lambda parameter_reader:
                       parameter_reader(opcode_parser),
                   self.parameter_readers)

    ###############################################

    def to_opcode(self, parameters):

        if self.opcode_class is not None:
            return self.opcode_class(* parameters)
        else:
            return None

#####################################################################################################
#
# End
#
#####################################################################################################
