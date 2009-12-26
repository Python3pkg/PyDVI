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
#####################################################################################################

from TfmParser import *

#####################################################################################################

# subprocess.call('kpsewhich', 'cmr10.tfm')

from optparse import OptionParser

usage = 'usage: %prog [options]'

parser = OptionParser(usage)

opt, args = parser.parse_args()

tfm_file_name = args[0]

tfm_file = TfmParser(tfm_file_name)

tfm_file.print_summary()

#####################################################################################################
#
# End
#
#####################################################################################################
