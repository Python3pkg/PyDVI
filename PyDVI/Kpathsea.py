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
#  - 26/12/2009 fabrice
#
#####################################################################################################

#####################################################################################################

import string
import subprocess

#####################################################################################################

def which(filename, format = None):

    '''
    Wrapper around kpsewhich program
    '''

    command = ['kpsewhich']

    if format is not None:
        command.append('--format=' + format)

    command.append(filename)

    command_string = string.join(command, sep=' ')

    pipe = subprocess.Popen(command_string, shell=True, stdout=subprocess.PIPE)
        
    stdout, stderr = pipe.communicate()

    path = stdout.rstrip()

    if len(path) > 0:
        return path
    else:
        return None

#####################################################################################################
#
#                                               Test
#
#####################################################################################################
        
if __name__ == '__main__':

    print 'kpsewhich cmr10.tfm', which('cmr10', format = 'tfm')

#####################################################################################################
#
# End
#
#####################################################################################################
