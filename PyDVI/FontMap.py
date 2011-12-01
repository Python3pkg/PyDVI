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
# - 01/11/2011 Fabrice
#   - check init definition
#
#####################################################################################################

"""
This module handles font map file.

A font map gives the correspondance between the TeX PK fonts and their PostScript equivalents. It
uses the ".map" extension.

For example, the file :file:`pdftex.map` contains lines like::

  futbo8r Utopia-Bold ".167 SlantFont TeXBase1Encoding ReEncodeFont" <8r.enc <putb8a.pfb

Each line describes a PK font using the following format::

  PK_FONT_NAME PS_FONT_NAME "PostScript snippet" <FILE_NAME1 <FILE_NAME2

The first word is the TeX font name and the second word is the PostScript font name. The PostScript
font name can be omitted if it is the same than the TeX font name. The word starting by '<' are
filenames to be included in the PostScript file. A filename with the extension '.enc' is an encoding
file and a filename with the extension '.pfb' is a Printer Font Binary file. The text enclosed by
double quotes is optional and gives a PostScript snippet to be inserted in the PostScript file. It
can be placed at the end of the line.

The percent character is used for comment as for TeX.

.. What is the source of this:
.. one or two '<'
.. This can be overridden with a left bracket: '<[encfile' indicates an encoding file named encfile.

References:

* The Font Installation Guide Using Postscript fonts to their full potential with Latex. Originally
  written by Philipp Lehman. December 2004. Revision 2.14. cf. Creating map files Part.
* updmap(1) - Update font map files for TeX output drivers.
* updmap.cfg(5) - configuration of font mapping/inclusion for dvips and friends

"""

#####################################################################################################

__all__ = ['FontMap', 'FontMapEntry']

#####################################################################################################

from PyDVI.Tools.Logging import print_card
from PyDVI.Tools.TexCommentedFile import TexCommentedFile

#####################################################################################################

class FontMapEntry(object):

    """ This class encapsulates a font map entry.
    
    Public attributes are:

      :attr:`tex_name`

      :attr:`ps_font_name`

      :attr:`ps_snippet`

      :attr:`effects`

      :attr:`encoding`

      :attr:`filename`
    """

    ###############################################

    def __init__(self, tex_name, ps_font_name, ps_snippet, effects, encoding, filename):

        self.tex_name = tex_name
        self.ps_font_name = ps_font_name
        self.ps_snippet = ps_snippet
        self.effects = effects
        self.encoding = encoding
        self.filename = filename

    ###############################################

    def print_summary(self):

        message_pattern = '''Font Map Entry %s

 - PS font name %s
 - ps snippet   "%s"
 - effects      %s
 - encoding     %s
 - filename     %s''' 

        message = message_pattern % (
            self.tex_name,
            self.ps_font_name,
            self.ps_snippet,
            self.effects,
            self.encoding,
            self.filename,
            )

        print_card(message)

#####################################################################################################

class FontMap(object):

    """ This class parses a fontmap file.

    A font map entry :class:`FontMapEntry` can be retrivied using the TeX name as key::

      font_map_instance[tex_name]
    """

    ###############################################

    def __init__(self, name, filename=None):

        self.name = name
        self._map = {}

        # Fixme: why?
        if filename is not None:
            #try:
            with TexCommentedFile(filename) as font_map_file:
                for line in font_map_file:
                    self._parse_line(line)
            #except:
            #    raise NameError('Bad fontmap file')

    ###############################################
 
    def __getitem__(self, tex_name):
 
        return self._map[tex_name]
 
    ###############################################
 
    def register_entry(self, font_map_entry):
 
        """ Register a font map entry.
        """

        self._map[font_map_entry.tex_name] = font_map_entry

    ###############################################
 
    def _parse_line(self, line):

        """ Parse a line:
        """

        # 1) Extract PostScript Snippet if there
        first_double_quote_index = line.find('"')
        if first_double_quote_index != -1:
            last_double_quote_index = line.find('"', first_double_quote_index+1)
            ps_snippet = line[first_double_quote_index+1:last_double_quote_index]
            effects = FontMap._parse_effects(ps_snippet)
            line = line[:first_double_quote_index] + line[last_double_quote_index+1:]
        else:
            ps_snippet = ''
            effects = {}
 
        sub_strings = [x.strip() for x in line.split('<')]
        if len(sub_strings) == 1:
            raise ValueError("Font map entry has any <FileNAME")
        right_part, filenames = sub_strings[0], sub_strings[1:]

        font_names = right_part.split()
        if len(font_names) == 2:
            tex_name, ps_font_name = font_names
        else:
            tex_name = ps_font_name = font_names[0]

        encoding_filename, pfb_filename = None, None
        for filename in filenames:
            if filename.startswith('['):
                assert encoding_filename is None
                encoding_filename = filename[1:]
            elif filename.endswith('.enc'):
                assert encoding_filename is None
                encoding_filename = filename
            elif filename.endswith('.pfb') or filename.endswith('.ttf'):
                assert pfb_filename is None
                pfb_filename = filename
            else:
                raise ValueError("Unknown file extension for file %s" % (filename))

        font_map_entry = FontMapEntry(tex_name, ps_font_name,
                                      ps_snippet, effects,
                                      encoding_filename, pfb_filename)
        self.register_entry(font_map_entry)
    
    ###############################################
    
    @staticmethod
    def _parse_effects(ps_snippet):

        """ Parse the PostScript snippet.
        """
 
        effects_list = ps_snippet.split()
        effects = {}
        for key_word in 'SlantFont', 'ExtendFont':
            try:
                # parameter is followed by the command
                parameter_index = effects_list.index(key_word) -1
                effects[key_word] = float(effects_list[parameter_index])
            except ValueError: # key word was not found
                pass
            
        return effects
    
    ###############################################
 
    def print_summary(self):
 
        print_card('Font Map %s' % (self.name))
 
        for font_map_entry in self._map.values():
            font_map_entry.print_summary()

#####################################################################################################
#
# End
#
#####################################################################################################
