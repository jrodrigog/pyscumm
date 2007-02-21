#    PySCUMM Engine. SCUMM based engine for Python
#    Copyright (C) 2006  PySCUMM Engine. http://pyscumm.org
#
#    This library is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Lesser General Public
#    License as published by the Free Software Foundation; either
#    version 2.1 of the License, or any later version.
#
#    This library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with this library; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

import pyscumm, random



class Playa( pyscumm.Room ):

    def init( self ):
        # Here write the sentences that Playa need to run right
        self.logo = pyscumm.sdl.Image( 'pyscumm/artwork/pyscumm_logo.tga' )
        #self.logo.set_pos( ( pyscumm.Engine().display.get_size()[0]/2, pyscumm.Engine().display.get_size()[1]/2, 0 ) )
        self.container.append( self.logo )

    def on_event( self, event_dict ):
        # Here intercept pyscumm events
        # if any double click event...
        if event_dict["type"] == pyscumm.DOUBLE_CLICK and event_dict["btn"] == 1:
            s = self.logo.get_size()
            # Change size image
            self.logo.set_size( (s[0]+50,s[1]+50) )
        elif event_dict["type"] == pyscumm.DOUBLE_CLICK and event_dict["btn"] == 3:
            s = self.logo.get_size()
            # Change size image
            self.logo.set_size( (s[0]+150,s[1]+50) )
        elif event_dict["type"] == pyscumm.DRAG_START:
            cur_pos = pyscumm.Engine().mouse.get_pos()
            self.logo.set_pos( (cur_pos[0], cur_pos[1], 0) )



# Mute the debugger
#pyscumm.Debugger().console = False

# Create a Engine
demo = pyscumm.Engine()
# Run the Engine with Playa Room
demo.run( Playa )
