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

#####################################################################################################

import sys

from optparse import OptionParser

#####################################################################################################

from PyDVI.Kpathsea import kpsewhich
from PyDVI.TfmParser import TfmParser

#####################################################################################################

usage = 'usage: %prog font_name'

parser = OptionParser(usage)

opt, args = parser.parse_args()

if len(args) != 1:
    parser.error("Give a a font name, e.g. cmr10")

font_name = args[0]

#####################################################################################################

tfm_file = kpsewhich(font_name, file_format='tfm')
if tfm_file is None:
    print 'TFM file %s not found' % (font_name)
    sys.exit(1)

tfm_parser = TfmParser()
tfm = tfm_parser.parse(font_name, tfm_file)
tfm.print_summary()

#####################################################################################################
#
# End
#
#####################################################################################################
