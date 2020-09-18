# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 20:25:08 2020

@author: Rushad
"""

import numpy as np
import sympy  
      
class CurrentSource():
    
    class DC():
        def __init__(self, current, name):
            self._t = np.arange(0, 20, 0.01)
            self._I = current*np.ones(len(self._t))
            self._name = sympy.core.symbols(name)
    
    class AC():        
        def __init__(self, peak_current, angular_freq, phase_angle, name):
            self._t = np.arange(0, 20, 0.01)
            self._I = peak_current*np.sin(self._angular_freq*self._t + self._phase_angle)
            self._name = sympy.core.symbols(name)
            
class VoltageSource():
    
    class DC():
        def __init__(self, voltage, name):
            self._t = np.arange(0, 20, 0.01)
            self._V = voltage*np.ones(len(self._t))
            self._name = sympy.core.symbols(name)
    
    class AC():        
        def __init__(self, peak_voltage, angular_freq, phase_angle, name):
            self._t = np.arange(0, 20, 0.01)
            self._V = peak_voltage*np.sin(self._angular_freq*self._t + self._phase_angle)
            self._name = sympy.core.symbols(name)

class Element():
    
    class Resistor():
        
        def __init__(self, resistance, name):
            self.resistance = resistance
            self._name = sympy.core.symbols(name)

    class Capacitor():
        def __init__(self, capacitance, name):
            self.capacitance = capacitance
            self._name = sympy.core.symbols(name)
        
    class Inductor():
        def __init__(self, inductance, name):
            self.inductance = inductance
            self._name = sympy.core.symbols(name)
            
class Circuit():

    class Mesh():
        
        def __init__(self):
            self._node = []
            self._temp_dict = {}
            self._element_index = 0
            
        def add(self, element, node1, node2):
            self._node1 = node1
            self._node2 = node2
            self._element = element
            
            # To add condition elem1 < > elem2
            #element_index 
            if len(self._node) == 0:
                self._temp_dict[str(self._node1) + str(self._node2)] = self._element
                temp_dict_copy = self._temp_dict.copy()
                self._node.append(temp_dict_copy)
                self._temp_dict.clear()
            else:
                self._temp_dict[str(self._node1) + str(self._node2)] = self._element
                temp_dict_copy = self._temp_dict.copy()
                self._node.append(temp_dict_copy)
                self._temp_dict.clear()
                self._element_index = self._element_index + 1

        def _getSource(self):
            
            if type(list(self._node[0].values())[0]) == CurrentSource.DC:
                source_type = 'cs'
            elif type(list(self._node[0].values())[0]) == CurrentSource.AC:
                source_type = 'cs'
            elif type(list(self._node[0].values())[0]) == VoltageSource.DC:
                source_type = 'vs'
            elif type(list(self._node[0].values())[0]) == VoltageSource.AC:
                source_type = 'vs'
            
            return source_type
            
        def solve(self):
            
            source = self._getSource()
            if source == 'cs':
                    
                temp_eq = 0
                temp_eq_list = []
                node_check = []
                
                for i in range(len(self._node)):
                    current_node = (list(self._node[i].keys())[0][0], list(self._node[i].keys())[0][1])
                    current_node_ep = current_node[1]
                    
                    for j in range(len(self._node)):
                        next_node = (list(self._node[j].keys())[0][0], list(self._node[j].keys())[0][1])
                        next_node_sp = next_node[0]
                        
                        if current_node_ep == next_node_sp:
                            
                            if type(list(self._node[i].values())[0]) == CurrentSource.DC or type(list(self._node[i].values())[0]) == CurrentSource.AC:
                                temp_eq = temp_eq + list(self._node[i].values())[0]._name
                                temp_eq_list.append(temp_eq)
                                temp_eq = 0
                            else:   
                                node1 = 'V' + str(current_node[0])
                                node2 = 'V' + str(current_node[1])
                                
                                node1 = sympy.core.symbols(node1)
                                node2 = sympy.core.symbols(node2)
                                
                                if len(node_check) == 0:
                                    node_check.append(node1)
                                    node_check.append(node2)
                                else:
                                    if node1 == node_check[0] or node2 == node_check[1]:
                                        impedance = list(self._node[i].values())[0]._name
                                        temp_eq  = temp_eq - (node1 - node2)/impedance
                                        temp_eq_list.append(temp_eq)
                                    else:
                                        impedance = list(self._node[i].values())[0]._name
                                        temp_eq  = temp_eq - (node1 - node2)/impedance
                                        temp_eq_list.append(temp_eq)
                                        temp_eq = 0
                                        node_check.clear()
                                
            return temp_eq_list
                    
                    