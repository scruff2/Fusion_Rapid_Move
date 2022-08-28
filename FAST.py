# WARNING : Use carefully.  If there is a problem with the GCODE produced by this software, Your CNC router may crash.
# WARNING : Use at your own risk.  This is experimental code and may damage your machine.
#
# The free license (hobbyist version) of Fusion 360 removes the rapid moves from the GCODE.
# A rapid move command is G00 or just G0.  Both formats work the same.
# Fusion 360 replaces these with a G1 command, causing your CNC to only run at your programmed feedrate,
# instead of at the rapid rate.  This can be a huge waste of time for large projects.
#
# This code is very specific to a pattern generated by Fusion 360, as of August 27, 2022.
# If Fusion 360 changes this pattern, then the GCODE output by this software must not be used.
#
# The pattern in the GCODE produced by Fusion is:
# GCODE Line N: Z Retract#  (Example: if 25.4 mm is your RETRACT setup value, this GCODE line will be Z25.4)
# GCODE Line N+1: Anything in this second line, usually X# Y#  (Example X6.953 Y6.564)
# GCODE Line N+2: Z# (Example: Z14.515)
#
# As this pattern is recognized, this software will add G00 in front of the Z Retract#
# and then will leave the next GCODE line alone
# and then will add G01 to the next line (this is the 2nd line after the Retract# was detected)
#
# How to use this software:
# The Fusion 360 generated GCODE must be saved as "input.nc" at the same location where
# this software is saved.
# Once the FAST.py Python code runs, the modified GCODE will be named "output.nc" and available at the same location.
#

retractZ = 24.5  # Change this to the value (millimeters) of the Retract height, as you have configured in Fusion 360.
outputLine = ''
flag = 0
f_output = open('output.nc', 'w')
with open('input.nc', 'r') as f:
    for line_raw in f:
        if flag == 2:  # Need to add G00 in front of the Z code. Ex.: Z11.846 needs to be G00 Z11.846
            flag = 1
        if flag == 3:  # This GCODE line does not need to be modified. Ex.: X98.761 Y142.561
            flag = 2
        line = line_raw.strip()
        if line == '':  # Adds a space if the line is blank.
            line = ' '
        # print(line)
        if line[0] == 'Z':
            zValue_list = line[1:].split(' ')
            zValue = float(zValue_list[0])
            # print(zValue)
            if zValue == retractZ:
                # print('Add G00', line)
                outputLine = 'G00 ' + line
                flag = 3
            elif (zValue < retractZ) and (flag == 1):
                outputLine = 'G01 ' + line
                flag = 0
            else:
                outputLine = line
        else:
            outputLine = line

        f_output.writelines(outputLine + '\n')
f_output.close()
