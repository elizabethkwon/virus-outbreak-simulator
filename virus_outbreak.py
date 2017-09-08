i#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 21:31:13 2017

@author: Sooyun
"""

#Name: Elizabeth Kwon
#Homework 4 

import random
import math
from matplotlib import pyplot as plt
#Add matplotlib inline


def normpdf(x, mean, sd):
    """
    Return the value of the normal distribution 
    with the specified mean and standard deviation (sd) at
    position x.
    You do not have to understand how this function works exactly. 
    """
    var = float(sd)**2
    denom = (2*math.pi*var)**.5
    num = math.exp(-(float(x)-float(mean))**2/(2*var))
    return num/denom

    
recovery_time = 4 # recovery time in time-steps
virality = 0.7    # probability that a neighbor cell is infected in 
                  # each time step                                                  

class Cell(object):

    def __init__(self,x, y):
        self.x = x
        self.y = y 
        self.state = "S" # can be "S" (susceptible), 
                         # "R" (resistant = dead), or "I" (infected)
        self.time = 0
        
    def infect(self):
        #Turn 'S' into 'I'
        self.state = "I"
        
    
    def process(self, adjacent_cells):
        
        #Only relevant is cell is 'I'
        if self.state == "I":
            self.time += 1
            for adjacent in adjacent_cells:
                #Check whether the random variable is less than virality
                #If so, it infects it
                if adjacent.state == 'S':
                    if random.random() <= virality:
                        adjacent.infect()
                
                #Check if the time counter is equal to
                #recovery time then change state to 'S'
                if self.time == recovery_time:
                   self.state = "S"
                   
                #If the time counter is not the same
                #check for the mortality
                else:
                    p_death = normpdf(self.time, 3, 1)
                    if random.random() < p_death:
                        self.state = 'R'        


        
class Map(object):
    
    def __init__(self):
        self.height = 150
        self.width = 150           
        self.cells = {}

    def add_cell(self, cell):
        
        #cells is accessible in the entire class Map.cell is accessible in only this add_cell function
        #The cells' dictionary key is represented by the object cell's x and y value
        #The value of cell's dictionary is the value that is being put in
        key = (cell.x, cell.y)
        self.cells[key] = cell
        
        pass
        
    def display(self):
        
        list_of_lists = []

        #Creating the 150 by 150 pixel row black grid 
        #Then setting the state exceptions for when 
        #the cell should be green, red or gray 
        for row_pixel in range(self.height):
            a_list = []
            for column_pixel in range(self.width):
                if (row_pixel,column_pixel) in self.cells.keys():
                    #If 'S' then green
                    if self.cells[(row_pixel,column_pixel)].state == 'S':
                        a_list.append((0.0,1.0,0.0))
                    #If "I" then red
                    if self.cells[(row_pixel,column_pixel)].state == 'I':
                        a_list.append((1.0,0.0,0.0))
                    #If "R" then gray
                    if self.cells[(row_pixel,column_pixel)].state == 'R':
                        a_list.append((0.5,0.5,0.5))    
                else:
                    a_list.append((0.0,0.0,0.0))
            
            list_of_lists.append(a_list)   
        
        plt.imshow(list_of_lists)
        
    
    def adjacent_cells(self, x, y):
        
        adjacent_cell_list = []
        
        #if the adjacent cell is to the left of the cell 
        #if the adjacent cell is to the right of th cell 
        #east
        if x + 1 < self.width:
            if (x+1, y) in self.cells.keys():
                east = self.cells[(x+1, y)]
                adjacent_cell_list.append(east)
        #west
        if x - 1 > 0:
            if (x-1, y) in self.cells.keys():
                west = self.cells[(x-1, y)]
                adjacent_cell_list.append(west)
            
        #if the adjacent cell is above the cell
        #if the adjacent cell is below the cell
        #north
        if y + 1 < self.height:
            if (x, y+1) in self.cells.keys():
                north = self.cells[(x, y+1)]
                adjacent_cell_list.append(north)
        #south
        if y - 1 > 0:
            if (x, y - 1) in self.cells.keys():
                south = self.cells[(x, y-1)]
                adjacent_cell_list.append(south)
        
        return adjacent_cell_list

    def time_step(self):
        #Should just call the process() method on each cell of the map
        #And then just calls display() to display the map
        for cell in self.cells:
            the_cell = self.cells[cell]
            the_cell.process(self.adjacent_cells(cell[0], cell[1]))
        self.display()
        
            
def read_map(filename):
    
    m = Map()
    
    #Reads the file
    cell_file = open(filename, 'r')
    
    #Takes in each line of the file and removes the comma within the file
    for line in cell_file:
        
        new_line = line.split(',')  
        
        #To create a new cell
        #This map contains all the cells from the file
        new_cell = Cell(int(new_line[0]),int(new_line[1]))
        m.add_cell(new_cell)
    
    return m

    
    
    
    
    
    
    
    
    
    
    
    
    