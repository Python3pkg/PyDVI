####################################################################################################
# 
# PyDvi - A Python Library to Process DVI Stream
# Copyright (C) 2014 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
####################################################################################################

####################################################################################################

import logging

import numpy as np

####################################################################################################

from PyOpenGLng.HighLevelApi import GL
from PyOpenGLng.HighLevelApi.Buffer import GlArrayBuffer
from PyOpenGLng.HighLevelApi.VertexArrayObject import GlVertexArrayObject

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class TextVertexArray(GlVertexArrayObject):

    """ This class wraps a Text Vertex Array. """

    _logger = _module_logger.getChild('TextVertexArray')

    ##############################################
    
    def __init__(self, image_texture, items=None):

        super(TextVertexArray, self).__init__()

        self._image_texture = image_texture # Fixme: could contains several font and size
        self._font_atlas_shape = image_texture.shape

        self._number_of_items = 0
        self._positions_buffer = GlArrayBuffer() # could pass data here
        self._texture_coordinates_buffer = GlArrayBuffer()
        self._colours_buffer = GlArrayBuffer()

        if items is not None:
            self.set(*items)

    ##############################################
    
    def set(self, positions, texture_coordinates, colours):

        """ Set the vertex array from a numpy array. """

        self._number_of_items = positions.shape[0]

        self._positions_buffer.set(positions)
        self._texture_coordinates_buffer.set(texture_coordinates)
        self._colours_buffer.set(colours)

    ##############################################
    
    def bind_to_shader(self, shader_program_interface):

        self.bind()

        shader_program_interface.position.bind_to_buffer(self._positions_buffer)
        shader_program_interface.position_uv.bind_to_buffer(self._texture_coordinates_buffer)
        shader_program_interface.colour.bind_to_buffer(self._colours_buffer)

        # Texture unit as default
        # shader_program.uniforms.texture0 = 0

        self.unbind()

    ##############################################
    
    def draw(self, shader_program):

        # Freetype renders glyph as grayscale: white foreground on black background
        #   If the LCD filter is enabled then the pixels on border are coloured.
        #   black fragment should be discarded
        #
        # Blending equation for transparency:
        #   O = (1-Sa)*D + Sa*S
        #     if Sa = 1 then O = S overwrite
        #           = 0 then O = D keep the value
        #
        # Grayscale case:
        #   S = luminosity * colour   grayscale = luminosity
        #   Sa = average luminosity * alpha ???
        #
        # LCD case:
        #   white -> red : (1,1,1) -> (1,0,0)

        # Blending: O = Sf*S + Df*D
        #  where S is the colour from the fragment shader and D the colour from the framebuffer
        #   alpha: fully transparent = 0 and fully opaque = 1
        #   Sa = average luminosity * colour aplha
        #
        # Set (Sf, Df) for transparency: O = Sa*S + (1-Sa)*D 

        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)

        shader_program.bind()
        self._image_texture.bind()
        self.bind()

        shader_program.uniforms.font_atlas = 0
        # shader_program.uniforms.gamma = 1.

        GL.glDrawArrays(GL.GL_POINTS, 0, self._number_of_items)

        self.unbind()
        self._image_texture.unbind()
        shader_program.unbind()

        GL.glDisable(GL.GL_BLEND)

####################################################################################################
# 
# End
# 
####################################################################################################
