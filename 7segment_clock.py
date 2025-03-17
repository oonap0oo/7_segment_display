#!/usr/bin/env python3
#
#  7segment_clock.py
#  
#  Copyright 2025 Nap0
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
# This Python code implements a digital clock with vintage looking seven segment display
# the seven segment display is drawn once a Tkinter canvas, the digits are then updated
# by switching their visibility on and off appropriately the logic for switching the segments
# in function of the character to be displayed is kept in a dictionary with the character als key
# and seven booleans representing the state of the seven segements for that character
#
import tkinter as tk
from tkinter import colorchooser
import time

class Clock(tk.Tk):
    def __init__(self):
        super().__init__()    
        self.title("Python seven-segment clock on a Tkinter Canvas")
        self.configure(bg="black",padx=8,pady=4)
        self.rowconfigure(0,weight=1)
        
        # am/pm of 24h time
        self.tktimemode = tk.StringVar()
        self.tktimemode.set("24h")
        
        # show the date i.s.o. time when boolean is true
        self.tkshowdate = tk.BooleanVar()
        self.tkshowdate.set(False)
        
        # set up menus
        self.menubar=tk.Menu(self, background="black", fg="#C0C0C0")
        self.menufile=tk.Menu(self.menubar,tearoff=0)
        self.menufile.add_command(label="Quit",command=self.destroy)
        self.menubar.add_cascade(label="File",menu=self.menufile)
        self.menusettings=tk.Menu(self.menubar,tearoff=0)
        self.menusettings.add_command(label="Color of display",command=self.setdisplaycolor)
        self.menusettings.add_separator()
        self.menusettings.add_radiobutton(label="24h time format",value="24h",variable=self.tktimemode)
        self.menusettings.add_radiobutton(label="12h am/pm time format",value="12h",variable=self.tktimemode)
        self.menusettings.add_separator()
        self.menusettings.add_checkbutton(label="Show date",variable=self.tkshowdate)
        self.menubar.add_cascade(label="Settings",menu=self.menusettings)   
        self.config(menu=self.menubar) 
        
        # color of 7 segement displays
        self.displaycolor="red"
        
        # initial size of canvas widgets
        self.CVSHEIGHT=200
        self.CVSWIDTH=125
        self.CVSDPWIDTH=30        
        
        # variable to keep track of which event is actual resize        
        self.h=0
        self.w=0
        
        # variable to keep track of wether double points are visible
        self.dpvisible=True
        
        # list to hold references to the Canvas widgets
        self.cv=[] 
        
        # variables containing the id of the canvas elents used for double points
        self.dp1=0
        self.dp2=0
        
        # which columns have to contain a full widh canvas for 7 segment displays
        cols=(0,1,3,4,6,7)
        
        # generate canvas elements for 7 segement displays, position them using grid() 
        # and configure columns for resizing using columnconfigure()
        for index in range(6):                
            self.cv.append( tk.Canvas(self,background="black",height=self.CVSHEIGHT,width=self.CVSWIDTH,bd=0, highlightthickness=0) )
            self.cv[index].grid(row=0,column=cols[index],sticky="WENS")
            self.columnconfigure(cols[index],weight=1)
        
        # generate canvas element for first double point, position it using grid() 
        # and configure column for resizing using columnconfigure()
        self.cvdp1 = tk.Canvas(self,background="black",height=self.CVSHEIGHT,width=self.CVSDPWIDTH,bd=0, highlightthickness=0)
        self.cvdp1.grid(row=0,column=2,sticky="WENS")
        self.columnconfigure(2,weight=1)
        
        # generate canvas element for second double point, position it using grid() 
        # and configure column for resizing using columnconfigure()
        self.cvdp2 = tk.Canvas(self,background="black",height=self.CVSHEIGHT,width=self.CVSDPWIDTH,bd=0, highlightthickness=0)
        self.cvdp2.grid(row=0,column=5,sticky="WENS")
        self.columnconfigure(5,weight=1)
        
        # draw segments and double point elements on the various canvas widgets
        self.updatealldisplays()
        
        # call self.resized method when the canvas generates a <Configure> event 
        self.cv[0].bind("<Configure>",self.resized)
        
        # call timerevent() to update display content for the first time        
        self.timerevent()  
        
    
    # called in time intervals using after() method
    def timerevent(self):
        self.updatetime()
        # call this function again after 500ms        
        self.after(500,self.timerevent)
        

    # update state of segments en double points to display current time
    def updatetime(self):
        
        # get date or one of the time formats
        if self.tkshowdate.get():
            # get curren date in format yymmdd
            now=time.strftime("%d%m%y")
        else:
            if self.tktimemode.get()=="24h":
                # get current time in format hhmmss, 24h format
                now=time.strftime("%H%M%S")
            elif self.tktimemode.get()=="12h":
                # get current time in format hhmmss, 12h am/pm format
                now=time.strftime('%I%M%S')
       
        # iterate through characters of time and update 7 segement displays with them
        for teller,digit in enumerate(now): # enumerate generates integer index
            self.sevensegmentupdate(self.cv[teller], digit)
        
        # toggle visibility of douple points every pass
        if self.dpvisible:
            self.cvdp1.itemconfig(self.dp1,state=tk.NORMAL)
            self.cvdp1.itemconfig(self.dp2,state=tk.NORMAL)
            self.cvdp2.itemconfig(self.dp1,state=tk.NORMAL)
            self.cvdp2.itemconfig(self.dp2,state=tk.NORMAL)
            self.dpvisible=False
        else:
            self.cvdp1.itemconfig(self.dp1,state=tk.HIDDEN)
            self.cvdp1.itemconfig(self.dp2,state=tk.HIDDEN)
            self.cvdp2.itemconfig(self.dp1,state=tk.HIDDEN)
            self.cvdp2.itemconfig(self.dp2,state=tk.HIDDEN)
            self.dpvisible=True
    
        
    # generate list of coordinates for a segment with parameters as arguments
    # coordinates depend on x,y position, lenght and orientation of the segment    
    def sevensegmentcoord(self,segx,segy,seglength,segvh="hor"):
        
        # how a segment looks
        hsegment=((0,0),(10,-10),(90,-10),(100,0),(90,10),(10,10))
        
        # scale factor to get wanted size
        scale=seglength/100.0
        
        # start filling list coords
        coord=[]
        if segvh=="hor":
            for x,y in hsegment:
                coord.append( int(x*scale+segx) )
                coord.append( int(y*scale+segy) )
        elif segvh=="ver":
            for x,y in hsegment:
                coord.append( int(y*scale+segx) )
                coord.append( int(x*scale+segy) )
        return(coord)
    
    
    # draw the 7 segments on the given canvas cvs with given color
    def sevensegmentinit(self,cvs,color):       
        
        # get the height of the canvas
        cvs.update()
        canvas_height=cvs.winfo_height()
        
        # where to put the upper left corner of set of segments
        xtop=canvas_height // 10 + 5
        ytop=xtop
        
        # what should the height of the set of segments be
        height = canvas_height - ytop - 5 * canvas_height // 40 - 2 * canvas_height // 20        
        
        # derive the width from the height of the display
        width=height//2
        
        # little gap between the segments is related to overal lenght
        gap=height//40
        
        # in case a resize occured delete previous version
        cvs.delete('all')
        
        # keep the id of the segments in a list for future modifications
        self.seg=[]
        
        # top horizontal segment
        coords=self.sevensegmentcoord(xtop+2*gap,ytop+gap,width,"hor")
        self.seg.append( cvs.create_polygon(coords, fill=color, state=tk.HIDDEN) ) 
        
        # left top segment
        coords=self.sevensegmentcoord(xtop+gap,ytop+2*gap,height//2,"ver")
        self.seg.append( cvs.create_polygon(coords, fill=color, state=tk.HIDDEN) )  
        
        # right top  segment
        coords=self.sevensegmentcoord(xtop+3*gap+width,ytop+2*gap,height//2,"ver")
        self.seg.append( cvs.create_polygon(coords, fill=color, state=tk.HIDDEN) )  
        
        # middle horizontal segment
        coords=self.sevensegmentcoord(xtop+2*gap,ytop+3*gap+height//2,width,"hor")
        self.seg.append( cvs.create_polygon(coords, fill=color, state=tk.HIDDEN) )
        
        # left bottom segment
        coords=self.sevensegmentcoord(xtop+gap,ytop+4*gap+height//2,height//2,"ver")
        self.seg.append( cvs.create_polygon(coords, fill=color, state=tk.HIDDEN) )  
        
        # right bottom segment
        coords=self.sevensegmentcoord(xtop+3*gap+width,ytop+4*gap+height//2,height//2,"ver")
        self.seg.append(cvs.create_polygon(coords, fill=color, state=tk.HIDDEN) )  
        
        # bottom horizontal segment
        coords=self.sevensegmentcoord(xtop+2*gap,ytop+5*gap+height,width,"hor")
        self.seg.append( cvs.create_polygon(coords, fill=color, state=tk.HIDDEN) )
    
    
    # update the 7 segment to display symbol if possible
    def sevensegmentupdate(self,cvs,symbol):
        # segment switching logic is kept in a dictionary 
        # the symbol to be displayed is the key
        # seven boolean values represent the on/off state of the segments
        # { "<symbol>":(<seg1>,<seg2>,<seg3>,<seg4>,<seg5>,<seg6>,<seg7>) }
        #    ---1---
        #   |       |
        #   2       3
        #   |       |
        #    ---4---
        #   |       |
        #   5       6
        #   |       |
        #    ---7---
        #
        segmentlogic={
            "0":(True,True,True,False,True,True,True),
            "1":(False,False,True,False,False,True,False),
            "2":(True,False,True,True,True,False,True),
            "3":(True,False,True,True,False,True,True),
            "4":(False,True,True,True,False,True,False),
            "5":(True,True,False,True,False,True,True),
            "6":(True,True,False,True,True,True,True),
            "7":(True,False,True,False,False,True,False),
            "8":(True,True,True,True,True,True,True),
            "9":(True,True,True,True,False,True,True),
            "A":(True,True,True,True,True,True,False),
            "B":(False,True,False,True,True,True,True),
            "C":(True,True,False,False,True,False,True),
            "D":(False,False,True,True,True,True,True),  
            "E":(True,True,False,True,True,False,True),   
            "F":(True,True,False,True,True,False,False),  
            " ":(False,False,False,False,False,False,False),
            "_":(False,False,False,False,False,False,True),
            "-":(False,False,False,True,False,False,False),
            "|":(False,True,False,False,True,False,False),
            "lower":(False,False,False,True,True,True,True),
            "upper":(True,True,True,True,False,False,False)
            }
        
        # if the symbol is supported, iterate through the segments
        # and change their state into tk.NORMAL or tk.HIDDEN as required
        if symbol in segmentlogic:
            for enabled,segment in zip(segmentlogic[symbol],self.seg):
                if enabled:
                    cvs.itemconfig(segment,state=tk.NORMAL)
                else:
                    cvs.itemconfig(segment,state=tk.HIDDEN)
    
    
    # draw the douple points on the given canvas cvs with color
    def dpinit(self,cvs,color):
        
        # get the height and width of the canvas
        cvs.update()
        canvas_height=cvs.winfo_height()
        canvas_width=cvs.winfo_width()
        halfheight=canvas_height//2
        halfwidth=canvas_width//2
        
        # the radius of the points
        radius=canvas_height//20
        
        # the half distance between the points
        distance=canvas_height//6
        
        # in case a resize occured delete previous version
        cvs.delete('all')
        
        # upper point
        self.dp1=cvs.create_oval(halfwidth-radius, halfheight-distance-radius,
                halfwidth+radius, halfheight-distance+radius,
                fill=color)
        
        # lower point    
        self.dp2=cvs.create_oval(halfwidth-radius, halfheight+distance-radius,
                halfwidth+radius, halfheight+distance+radius,
                fill=color)
                
    
    # redraw all displays on the varous canvas widgets            
    def updatealldisplays(self):
        for cvs in self.cv: # redraw displays with new size
            self.sevensegmentinit(cvs,self.displaycolor)  
        self.dpinit(self.cvdp1,self.displaycolor) # redraw douple points with new size
        self.dpinit(self.cvdp2,self.displaycolor) 
        self.updatetime()


    # called when the canvas generates a <Configure> event 
    def resized(self,event):
        if (self.h!=event.height) or (self.w!=event.width): # see if this is a resize event
            self.h, self.w = event.height, event.width
            self.updatealldisplays()
    
    
    # called after selecting display color menu option
    def setdisplaycolor(self):
        answer=colorchooser.askcolor(self.displaycolor) # use colorchhoser dialogbox
        if not(answer[1] is None): # was an answer given?
            self.displaycolor=answer[1]
            self.updatealldisplays()
            

       
clock=Clock()
clock.mainloop()
