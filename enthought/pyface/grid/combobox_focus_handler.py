#------------------------------------------------------------------------------
# Copyright (c) 2005, Enthought, Inc.
# All rights reserved.
# 
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
# 
# Author: Enthought, Inc.
# Description: <Enthought pyface package component>
#------------------------------------------------------------------------------
""" Workaround for combobox focus problem in wx 2.6. """

# Major package imports
import wx

#-------------------------------------------------------------------------------
#  Constants:
#-------------------------------------------------------------------------------

# Mapping from key code to key event handler names:
Handlers = {
    wx.WXK_LEFT:   '_left_key',
    wx.WXK_RIGHT:  '_right_key',
    wx.WXK_UP:     '_up_key',
    wx.WXK_DOWN:   '_down_key',
    wx.WXK_ESCAPE: '_escape_key'  
}

#-------------------------------------------------------------------------------
#  'ComboboxFocusHandler' class:
#-------------------------------------------------------------------------------

class ComboboxFocusHandler(wx.EvtHandler):
    
    def __init__(self, grid):
        wx.EvtHandler.__init__(self)
        
        self._grid = grid
        wx.EVT_KEY_DOWN(self, self._on_key)
    
    def _on_key(self, evt):
        """ Called when a key is pressed. """
        # This changes the behaviour of the <Enter> and <Tab> keys to make
        # manual data entry smoother!
        #
        # Don't change the behavior if the <Control> key is pressed as this
        # has meaning to the edit control.
        getattr( self, Handlers.get( evt.GetKeyCode(), '_ignore_key' ))( evt )
            
#-- Key Event Handlers --------------------------------------------------------

    def _ignore_key ( self, evt ):
        evt.Skip()
        
    def _escape_key ( self, evt ):
        self._grid.DisableCellEditControl()
        
    def _left_key ( self, evt ):
        if not evt.ControlDown():
            evt.Skip()
            return
            
        grid, row, col, rows, cols = self._grid_info()
        
        col -= 1
        if col < 0:
            col  = cols - 1
            row -= 1
            if row < 0:
                row = rows - 1
                
        self._edit_cell( row, col )
        
    def _right_key ( self, evt ):
        if not evt.ControlDown():
            evt.Skip()
            return
            
        grid, row, col, rows, cols = self._grid_info()
        
        col += 1
        if col >= cols:
            col  = 0
            row += 1
            if row >= rows:
                row = 0
                
        self._edit_cell( row, col )
        
    def _up_key ( self, evt ):
        if not evt.ControlDown():
            evt.Skip()
            return
            
        grid, row, col, rows, cols = self._grid_info()
        
        row -= 1
        if row < 0:
            row = rows - 1
            
        self._edit_cell( row, col )
        
    def _down_key ( self, evt ):
        if not evt.ControlDown():
            evt.Skip()
            return
            
        grid, row, col, rows, cols = self._grid_info()
        
        row += 1
        if row >= rows:
            row = 0
            
        self._edit_cell( row, col )
        
#-- Private Methods -----------------------------------------------------------

    def _grid_info ( self ):
        g = self._grid
        return ( g, g.GetGridCursorRow(), g.GetGridCursorCol(),
                    g.GetNumberRows(),    g.GetNumberCols() )

    def _edit_cell ( self, row, col ):
        self._grid.SetGridCursor( row, col )
        self._grid.EnableCellEditControl()
        self._grid.MakeCellVisible( row, col )
        
#### EOF ####################################################################
