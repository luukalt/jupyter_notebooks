# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 16:49:55 2020

@author: laaltenburg
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import pandas as pd

#%% START

# Close all windows
plt.close('all')

#%% COLUMN INDICES OF DATA FILE
index_time = 0          # 0. 	Time [hh:mm:ss.xxx]
index_T_u = 1           # 1. 	Ambient Temperature T_u [K]
index_p_u = 2           # 2. 	Ambient Pressure p_u [Pa]
index_f_H2_set = 3      # 3.	Volume fraction of hydrogen of total fuel [-]
index_f_CH4DNG_set = 4  # 4. 	Volume fraction of methane in DNG [-]
index_f_C2H6DNG_set = 5 # 5. 	Volume fraction of ethane in DNG [-]
index_f_N2DNG_set = 6   # 6. 	Volume fraction of nitrogen in DNG [-]
index_D1 = 7            # 7. 	D1 [mm]
index_D2 = 8            # 8. 	D2 [mm]
index_H_liner = 9       # 9. 	H_liner [mm]
index_phi_set = 10      # 10.	Set equivalence ratio [-]
index_u_u_set = 11      # 11.	Set velocity u1 [m/s]	
index_phi_meas = 12     # 12.	Measured equivalence ratio [-]
index_u_u_meas = 13     # 13.	Measured velocity u1 [m/s]
index_f_H2_meas = 14     # 14.	Measured volume fraction of hydrogen
index_Q_air1_nL_per_min_meas = 15   # 15. 	Measured Air flow 1 [ln/min]
index_Q_air2_nL_per_min_meas  = 16  # 16. 	Measured Air flow 2 [ln/min]
index_Q_DNG_nL_per_min_meas  = 17   # 17. 	Measured DNG flow [ln/min]
index_Q_H2_nL_per_min_meas  = 18    # 18. 	Measured Hydrogen flow [ln/min]
index_m_mix_dot_meas  = 19          # 19.	Measured total mass flow of unburnt mixture [kg/s]
index_m_air1_dot_meas = 20          # 20.	Measured air mass flow of unburnt mixture [kg/s]
index_m_fuel_dot_meas = 21          # 21.	Measured fuel mass flow of unburnt mixture [kg/s]
index_P_thermal_meas = 22           # 22.	Measured thermal power output
index_rho_mix_meas = 23             # 23.	Measured density of unburnt mixture [kg/m^3]
index_LHV_H2= 24                    # 24.	LHV hydrogen [MW]
index_LHV_CH4 = 25                  # 25.	LHV methane [MW]
index_LHV_C2H6 = 26                 # 26. 	LHV ethane [MW]

variables_list = ['time', 'T_u_ambient', 'p_u_ambient', 'x_H2_set', 'x_CH4_set', 'x_C2H6_set', 'x_N2_set', 'D_inner_set', 'D_outer_set', 'H_liner_meas', 'phi_set', 'u_u_set',
                  'phi_meas', 'u_u_meas', 'x_H2_meas', 'Q_a1_meas', 'Q_a2_meas', 'Q_DNG_meas', 'Q_H2_meas',
                  'm_mix_dot_meas', 'm_a_dot_meas', 'm_f_dot_meas', 'power_meas', 'rho_u_meas', 'LHV_H2', 'LHV_CH4', 'LHV_C2H6']
        

# Important indices regarding flashback
index_u_u_design = 0
index_u_u_first_sign_FB = 1 
index_u_u_FB = 2
index_data = -1

#%% CONSTANTS
# T_STP = 273.15 K (= 0 C)
# p_STP = 101325 Pa
# R = 8.314 Pa*m^3/(K*mol)

#%% FORMULAS LABVIEW CONTROL PANEL
# Standard conditions correction:
# STP = (T_u/T_STP)*(p_STP/p_u)

# Molar volume:
# V_m = V/n = R*T_u/p_u

#%% LIBRARY OF EXPERIMENTAL DATA
# Initialize data library
flashback_data = {}

#  Dictionary with four keys: 
# - key1: hydrogen content
# - key2: phi
# - key3: test nr
# - key4: date
#
# and 5 values:
# - value1 = phi
# - value2 = frame index design point
# - value3 = frame index first sign of flashback point
# - value4 = frame index flashback point

# Fill library with experimental data
# H0
flashback_data[('H0', '0.60', '1', '2020-07-30')] = [285, None,  475]
flashback_data[('H0', '0.70', '1', '2020-07-28')] = [935 , None, 3670]
flashback_data[('H0', '0.70', '2', '2020-07-30')] = [431, None, 1495]
flashback_data[('H0', '0.80', '1', '2020-07-28')] = [242, 890, 2037]
flashback_data[('H0', '0.80', '2', '2020-07-30')] = [320, None, 1068]
flashback_data[('H0', '0.90', '1', '2020-07-28')] = [540, 1050, 2510]
flashback_data[('H0', '0.90', '2', '2020-07-30')] = [170, 447, 1175]
flashback_data[('H0', '1.00', '1', '2020-07-28')] = [660, 965, 1615]
flashback_data[('H0', '1.00', '2', '2020-07-30')] = [420, None, 1394]

# H25
flashback_data[('H25', '0.50', '1', '2020-07-29')] = [None, None, 280]
flashback_data[('H25', '0.50', '2', '2020-07-30')] = [None, None, 372]
flashback_data[('H25', '0.60', '1', '2020-07-29')] = [372, None, 1092]
flashback_data[('H25', '0.60', '2', '2020-07-30')] = [205, None, 1321]
flashback_data[('H25', '0.70', '1', '2020-07-29')] = [340, None, 642]
flashback_data[('H25', '0.70', '2', '2020-07-30')] = [240, None, 464]
flashback_data[('H25', '0.80', '1', '2020-07-29')] = [445, 1167, 1427]
flashback_data[('H25', '0.80', '2', '2020-07-30')] = [230, None, 595]
flashback_data[('H25', '0.90', '1', '2020-07-29')] = [770, 1442, 2179]
flashback_data[('H25', '0.90', '2', '2020-07-30')] = [327, 770, 1499]
flashback_data[('H25', '1.00', '1', '2020-07-29')] = [669, 1560, 2408]

# H50
flashback_data[('H50', '0.50', '1', '2020-07-28')] = [585, 815, 1425]
flashback_data[('H50', '0.50', '2', '2020-07-30')] = [600, 1210, 1610]
flashback_data[('H50', '0.60', '1', '2020-07-29')] = [760, None, 1402]
flashback_data[('H50', '0.60', '2', '2020-07-30')] = [510, None, 957]
flashback_data[('H50', '0.70', '1', '2020-07-28')] = [358, 1340, 2036]
flashback_data[('H50', '0.70', '2', '2020-07-30')] = [280, 1025, 1432]
flashback_data[('H50', '0.80', '1', '2020-07-29')] = [30, 470, 1911]
flashback_data[('H50', '0.80', '2', '2020-07-30')] = [90, 525, 1001]
flashback_data[('H50', '0.90', '1', '2020-07-28')] = [290, 1260, 2805]
flashback_data[('H50', '0.90', '2', '2020-07-30')] = [360, 720, 1485]

# H75
flashback_data[('H75', '0.35', '1', '2020-07-29')] = [1770, None, 2025]
flashback_data[('H75', '0.35', '2', '2020-07-30')] = [819, None, 1305]
flashback_data[('H75', '0.35', '3', '2020-07-31')] = [562, None, 951]
flashback_data[('H75', '0.40', '1', '2020-07-29')] = [1600, 2222, 2640]
flashback_data[('H75', '0.40', '2', '2020-07-30')] = [977, 1560, 1697]
flashback_data[('H75', '0.40', '3', '2020-07-31')] = [369, 730, 1136]
flashback_data[('H75', '0.50', '1', '2020-07-29')] = [64, 474, 1139]
flashback_data[('H75', '0.50', '2', '2020-07-30')] = [95, 798, 1355]
flashback_data[('H75', '0.50', '3', '2020-07-31')] = [None, 103, 788]
flashback_data[('H75', '0.60', '1', '2020-07-29')] = [None, 1110, 2405]
flashback_data[('H75', '0.60', '2', '2020-07-30')] = [None, 450, 1253]
flashback_data[('H75', '0.60', '3', '2020-07-31')] = [None, 89, 435]
flashback_data[('H75', '0.70', '1', '2020-07-29')] = [None, None, 82]
flashback_data[('H75', '0.70', '2', '2020-07-29')] = [None, None, 101]

# H100
# flashback_data[('H100', '0.30', '1', '2020-07-28')] = [None, None, 3198]
flashback_data[('H100', '0.30', '2', '2020-07-28')] = [None, None, 700]
flashback_data[('H100', '0.30', '3', '2020-07-30')] = [None, None, 762]
flashback_data[('H100', '0.30', '4', '2020-07-31')] = [None, None, 1230]
flashback_data[('H100', '0.35', '1', '2020-07-29')] = [None, None, 1385]
flashback_data[('H100', '0.35', '2', '2020-07-30')] = [None, None, 520]
flashback_data[('H100', '0.35', '3', '2020-07-31')] = [None, None, 1188]
flashback_data[('H100', '0.40', '1', '2020-07-28')] = [None, 2309, 2786] 
flashback_data[('H100', '0.40', '2', '2020-07-30')] = [None, None, 2003]
flashback_data[('H100', '0.40', '3', '2020-07-30')] = [None, 530, 1015]
flashback_data[('H100', '0.40', '4', '2020-07-31')] = [None, None, 1236]
flashback_data[('H100', '0.50', '1', '2020-07-28')] = [None, None, 896, 99]
flashback_data[('H100', '0.50', '2', '2020-07-28')] = [None, None, 1942, 99]


for key, value in flashback_data.items():
    
    hydrogen_percentage = key[0]
    phi = key[1]
    test_nr = key[2]
    date = key[3]
    
    # Directory of data
    data_dir = 'session_' + str(date) + '/'
    
    # A: File name of all data (except temperature)
    filename_A =  data_dir + str(hydrogen_percentage) + '_phi=' + str(phi) + '_u1=x_' + str(date) + '_test' + str(test_nr) + '.txt'
    
    # Read data of experiment
    data_A = pd.read_csv(filename_A, header=None)
    flashback_data[key].append(data_A)

#%% RESULTS: PLOT CONFIGURATION
# Directory to save figures
figure_folder = 'figures'
# Colors for test numbers
test_nr1_color = '#DB4437' # HEX color (google red: #DB4437)
test_nr2_color = '#4285F4' # HEX color (google blue: #4285F4)
test_nr3_color = '#0F9D58' # HEX color (google green: #0F9D58)
test_nr4_color = '#F4B400' # HEX color (google yellow: #F4B400)

# Color for hydrogen content in plot
H0_color = '#000000'
H25_color = '#4285F4'
H50_color = '#DB4437'
H75_color = '#F4B400'
H100_color = '#0F9D58'

# Titles for plots
H0_title = 'Hydrogen percentage = 0%'
H25_title = 'Hydrogen percentage = 25%'
H50_title = 'Hydrogen percentage = 50%'
H75_title = 'Hydrogen percentage = 75%'
H100_title = 'Hydrogen percentage = 100%'

# Label settings for plot legends
label_added_H0 = False
label_added_H25 = False
label_added_H50 = False
label_added_H75 = False
label_added_H100 = False

H0_label = 'H2% = 0'
H25_label = 'H2% = 25'
H50_label = 'H2% = 50'
H75_label = 'H2% = 75'
H100_label = 'H2% = 100'

# Marker types
design_point_marker = 'v'
first_sign_FB_marker = '*'
FB_marker = '^'
legend_markers = [Line2D([0], [0], marker=design_point_marker, color='w', label='Design point (stable operation)', markerfacecolor='k', markersize=12),\
                  Line2D([0], [0], marker=first_sign_FB_marker, color='w', label='First sign of FB', markerfacecolor='k', markersize=12),\
                  Line2D([0], [0], marker=FB_marker, color='w', label='FB', markerfacecolor='k', markersize=12)]
    
#%% RESULTS: A
for key, value in flashback_data.items():
    
    if key[0] == 'H0':
        plt.figure(1)
        x_lim_left = 0.50
        x_lim_right = 1.10
        y_lim = 2
        fig_title = H0_title
    elif key[0] =='H25':
        plt.figure(2)
        x_lim_left = 0.40
        x_lim_right = 1.10
        y_lim = 3.5
        fig_title = H25_title
    elif key[0] =='H50':
        plt.figure(3)
        x_lim_left = 0.40
        x_lim_right = 1.00
        y_lim = 4.5
        fig_title = H50_title
    elif key[0] =='H75':
        plt.figure(4)
        x_lim_left = 0.30
        x_lim_right = 0.75
        y_lim = 7.00
        fig_title = H75_title
    elif key[0] =='H100':
        plt.figure(5)
        x_lim_left = 0.25
        x_lim_right = 0.55
        y_lim = 9.00
        fig_title = H100_title
        
    if key[2] == '1':
        marker_color = test_nr1_color
    elif key[2] == '2':
        marker_color = test_nr2_color
    elif key[2] == '3':
        marker_color = test_nr3_color
    elif key[2] == '4':
        marker_color = test_nr4_color
        
    if value[index_u_u_design] == None and value[index_u_u_first_sign_FB] == None:
        phi_FB = flashback_data[key][index_data][index_phi_meas][value[index_u_u_FB]]
        u_u_FB = flashback_data[key][index_data][index_u_u_meas][value[index_u_u_FB]]
        plt.plot(phi_FB, u_u_FB, color=marker_color, marker=FB_marker)
    elif value[index_u_u_design] == None:
        phi_first_sign_FB = flashback_data[key][index_data][index_phi_meas][value[index_u_u_first_sign_FB]]
        u_u_first_sign_FB = flashback_data[key][index_data][index_u_u_meas][value[index_u_u_first_sign_FB]]
        phi_FB = flashback_data[key][index_data][index_phi_meas][value[index_u_u_FB]]
        u_u_FB = flashback_data[key][index_data][index_u_u_meas][value[index_u_u_FB]]
        plt.plot(phi_first_sign_FB, u_u_first_sign_FB, color=marker_color, marker=first_sign_FB_marker)
        plt.plot(phi_FB, u_u_FB, color=marker_color, marker=FB_marker)
    elif value[index_u_u_first_sign_FB] == None:
        phi_design = flashback_data[key][index_data][index_phi_meas][value[index_u_u_design]]
        u_u_design = flashback_data[key][index_data][index_u_u_meas][value[index_u_u_design]]
        phi_FB = flashback_data[key][index_data][index_phi_meas][value[index_u_u_FB]]
        u_u_FB = flashback_data[key][index_data][index_u_u_meas][value[index_u_u_FB]]
        plt.plot(phi_design, u_u_design, color=marker_color, marker=design_point_marker)
        plt.plot(phi_FB, u_u_FB, color=marker_color, marker=FB_marker)
    else:
        phi_design = flashback_data[key][index_data][index_phi_meas][value[index_u_u_design]]
        u_u_design = flashback_data[key][index_data][index_u_u_meas][value[index_u_u_design]]
        phi_first_sign_FB = flashback_data[key][index_data][index_phi_meas][value[index_u_u_first_sign_FB]]
        u_u_first_sign_FB = flashback_data[key][index_data][index_u_u_meas][value[index_u_u_first_sign_FB]]
        phi_FB = flashback_data[key][index_data][index_phi_meas][value[index_u_u_FB]]
        u_u_FB = flashback_data[key][index_data][index_u_u_meas][value[index_u_u_FB]]
        plt.plot(phi_design, u_u_design, color=marker_color, marker=design_point_marker)
        plt.plot(phi_first_sign_FB, u_u_first_sign_FB, color=marker_color, marker=first_sign_FB_marker)
        plt.plot(phi_FB, u_u_FB, color=marker_color, marker=FB_marker)

    plt.xlabel('$\phi$ [-]')
    plt.ylabel('Unburned mixture bulk velocity $u_u$ [m/s]')
    plt.xlim(x_lim_left, x_lim_right)
    plt.ylim(0, y_lim)
    plt.grid(b=True, which='major', color='#666666', linestyle='--', axis='both')
    
    plt.legend(handles=legend_markers)
    plt.title(fig_title)

#%% RESULTS: FLASHBACK PROPENSITY MAP FOR VARYING HYDROGEN CONTENT AND PHI at FB
index = index_u_u_FB 
    
for key, value in flashback_data.items():
    
    plt.figure(6)
    
    if key[0] == 'H0':
        label_added = label_added_H0
        marker_color = H0_color
        label_text = H0_label
    elif key[0] == 'H25':
        label_added = label_added_H25
        marker_color = H25_color
        label_text = H25_label
    elif key[0] == 'H50':
        label_added = label_added_H50
        marker_color = H50_color
        label_text = H50_label
    elif key[0] == 'H75':
        label_added = label_added_H75
        marker_color = H75_color
        label_text = H75_label
    elif key[0] == 'H100':
        label_added = label_added_H100
        marker_color = H100_color
        label_text = H100_label
        
    phi_FB = flashback_data[key][index_data][index_phi_meas][value[index]]
    u_u_FB = flashback_data[key][index_data][index_u_u_meas][value[index]]
        
    if not label_added: 
        plt.plot(phi_FB, u_u_FB, color=marker_color, marker='^', label=label_text )
        if key[0] == 'H0':
            label_added_H0 = True
        elif key[0] == 'H25':
            label_added_H25 = True
        elif key[0] == 'H50':
            label_added_H50 = True
        elif key[0] == 'H75':
            label_added_H75 = True
        elif key[0] == 'H100':
            label_added_H100 = True
    else:
        plt.plot(phi_FB, u_u_FB, color=marker_color, marker=FB_marker)
    
    plt.xlabel('$\phi$ [-]')
    plt.ylabel('$u_{u,{FB}}$ [m/s]')
    plt.xlim(0.25, 1.1)
    plt.ylim(0, 9.00)
    plt.grid(b=True, which='major', color='#666666', linestyle='--', axis='both')
    plt.legend()
    plt.title('Flashback propensity map for multiple mixtures')

# Label settings for plot legends
label_added_H0 = False
label_added_H25 = False
label_added_H50 = False
label_added_H75 = False
label_added_H100 = False

# Save figure as .PNG
figure_name = 'FB_map'
plt.savefig(figure_folder +'/' + figure_name + '.png')
#%% RESULTS: FLASHBACK PROPENSITY MAP FOR VARYING HYDROGEN CONTENT AND PHI at design point
index = index_u_u_design 
    
for key, value in flashback_data.items():
    
    plt.figure(7)
    
    if not value[index] == None:
        
        if key[0] == 'H0':
            label_added = label_added_H0
            marker_color = H0_color
            label_text = H0_label
        elif key[0] == 'H25':
            label_added = label_added_H25
            marker_color = H25_color
            label_text = H25_label
        elif key[0] == 'H50':
            label_added = label_added_H50
            marker_color = H50_color
            label_text = H50_label
        elif key[0] == 'H75':
            label_added = label_added_H75
            marker_color = H75_color
            label_text = H75_label
        elif key[0] == 'H100':
            label_added = label_added_H100
            marker_color = H100_color
            label_text = H100_label
            
        phi_FB = flashback_data[key][index_data][index_phi_meas][value[index]]
        u_u_FB = flashback_data[key][index_data][index_u_u_meas][value[index]]
            
        if not label_added: 
            plt.plot(phi_FB, u_u_FB, color=marker_color, marker='^', label=label_text )
            if key[0] == 'H0':
                label_added_H0 = True
            elif key[0] == 'H25':
                label_added_H25 = True
            elif key[0] == 'H50':
                label_added_H50 = True
            elif key[0] == 'H75':
                label_added_H75 = True
            elif key[0] == 'H100':
                label_added_H100 = True
        else:
            plt.plot(phi_FB, u_u_FB, color=marker_color, marker=FB_marker)
        
        plt.xlabel('$\phi$ [-]')
        plt.ylabel('$u_{u,{FB}}$ [m/s]')
        plt.xlim(0.25, 1.1)
        plt.ylim(0, 9.00)
        plt.grid(b=True, which='major', color='#666666', linestyle='--', axis='both')
        plt.legend()
        plt.title('Flashback propensity map for multiple mixtures')
        
    elif value[index] == None:
        pass
    
#%%RESULTS: THERMAL POWER OUTPUT FOR VARYING HYDROGEN CONTENT AND  PHI at FB
# Intitalize variables (lists) to be plotted
phi_FB_list = []
u_u_FB_list = []
p_thermal_list = []   
index = index_u_u_FB  

for key, value in flashback_data.items():
    phi_FB = flashback_data[key][index_data][index_phi_meas][value[index]]
    u_u_FB = flashback_data[key][index_data][index_u_u_meas][value[index]]
    P_thermal_FB = flashback_data[key][index_data][index_P_thermal_meas][value[index]]
    
    phi_FB_list.append(phi_FB)
    u_u_FB_list.append(u_u_FB)
    p_thermal_list.append(P_thermal_FB)
    
plt.figure(8)  

sc = plt.scatter(phi_FB_list, u_u_FB_list, c=p_thermal_list, cmap='coolwarm',vmin=0, vmax=20)
cbar = plt.colorbar(sc)
cbar.set_label('Thermal power output [kW]')

plt.xlabel('$\phi$ [-]')
plt.ylabel('$u_{u,{FB}}$ [m/s]')
plt.xlim(0.25, 1.1)
plt.ylim(0, 9.00)
plt.grid(b=True, which='major', color='#666666', linestyle='-', axis='both')
plt.title('Flashback propensity map for multiple mixtures')
    
#%%RESULTS: THERMAL POWER OUTPUT FOR VARYING HYDROGEN CONTENT AND  PHI at design point
# Intitalize variables (lists) to be plotted
phi_FB_list = []
u_u_FB_list = []
P_thermal_list = []   
index = index_u_u_design 

for key, value in flashback_data.items():
    if not value[index] == None:
        phi_FB = flashback_data[key][index_data][index_phi_meas][value[index]]
        u_u_FB = flashback_data[key][index_data][index_u_u_meas][value[index]]
        P_thermal_FB = flashback_data[key][index_data][index_P_thermal_meas][value[index]]
        
        phi_FB_list.append(phi_FB)
        u_u_FB_list.append(u_u_FB)
        P_thermal_list.append(P_thermal_FB)
    elif value[index] == None:
        pass
    
plt.figure(10)  

sc = plt.scatter(phi_FB_list, u_u_FB_list, c=P_thermal_list, cmap='coolwarm',vmin=0, vmax=20)
cbar = plt.colorbar(sc)
cbar.set_label('Thermal power output [kW]')

plt.xlabel('$\phi$ [-]')
plt.ylabel('$u_{u,{FB}}$ [m/s]')
plt.xlim(0.25, 1.1)
plt.ylim(0, 9.00)
plt.grid(b=True, which='major', color='#666666', linestyle='-', axis='both')
plt.title('Flashback propensity map for multiple mixtures')

#%%RESULTS: AIR FLOW 1 FOR VARYING HYDROGEN CONTENT AND  PHI at FB
# Intitalize variables (lists) to be plotted
phi_list = []
u_u_list = []
Q_air1_nL_per_min_meas_list = []   
index = index_u_u_FB

for key, value in flashback_data.items():
    phi_FB = flashback_data[key][index_data][index_phi_meas][value[index]]
    u_u_FB = flashback_data[key][index_data][index_u_u_meas][value[index]]
    Q_air1_nL_per_min_meas_FB = flashback_data[key][index_data][index_Q_air1_nL_per_min_meas][value[index]]
    
    phi_list.append(phi_FB)
    u_u_list.append(u_u_FB)
    Q_air1_nL_per_min_meas_list.append(Q_air1_nL_per_min_meas_FB)
    
plt.figure(11)  

sc = plt.scatter(phi_list, u_u_list, c=Q_air1_nL_per_min_meas_list, cmap='coolwarm',vmin=0, vmax=1000)
cbar = plt.colorbar(sc)
cbar.set_label('Air flow 1 [Ln/min]')

plt.xlabel('$\phi$ [-]')
plt.ylabel('$u_{u,{FB}}$ [m/s]')
plt.xlim(0.25, 1.1)
plt.ylim(0, 9.00)
plt.grid(b=True, which='major', color='#666666', linestyle='-', axis='both')
plt.title('Flashback propensity map for multiple mixtures')
      
#%% RESULTS: PLOT SPECIFIC VARIABLE IN TIME DURING EXPERIMENT
plt.figure(12) 

experiment = ('H100', '0.35', '1', '2020-07-29')      
key = experiment     
t = flashback_data[key][index_data][index_time]
y1 = flashback_data[key][index_data][index_Q_air1_nL_per_min_meas]
y2 = flashback_data[key][index_data][index_Q_H2_nL_per_min_meas] 
y3 = flashback_data[key][index_data][index_Q_DNG_nL_per_min_meas] 
plt.plot(t, y1, label='Q_air')   
plt.plot(t, y2, label='Q_H2')   
plt.plot(t, y3, label='Q_DNG')   
plt.xlim(0, len(t))
plt.xticks(np.array([0, len(t)-1]))    
plt.legend()    

#%% RESULTS: PLOT SPECIFIC VARIABLE IN TIME DURING EXPERIMENT
plt.figure(13) 

plt.plot(t, y1/y2, label='Q_air/Q_H2')   
plt.xlim(0, len(t))
plt.xticks(np.array([0, len(t)-1]))    
plt.legend()        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    



