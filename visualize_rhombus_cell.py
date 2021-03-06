#!/usr/bin/env python
# -*- coding=UTF-8 -*-
"""
Parses an json file of input settings for Abinit,
determines positions of atoms within a unit cell from the "meta.atoms" data,
and displays those atoms in a 60° rhombus unit cell.

This input format is indicated by the .abinit.json format.
See 'generate_abinit_input_file_from_json.py' for details.

Atoms are specified using the 'atoms' attribute within 'meta', like so:

{
    "direct": [ ... ],
    "meta": {
        ...
        "atoms" : [
            <atoms attributes>
        ]
    }
}

Each atom is specified in the following way:
{
    "znucl":<nuclear charge:int>,
    "coord":<coordinate>
}

See 'convert_abinit_input_from_atoms_to_direct.py' for more details.
"""


__version__ = "0.0.0"

__author__ = "JJ Brown"
__copyright__ = "Copyright 2017, JJ Brown"
__credits__ = ["JJ Brown"]
__license__ = "MIT"
__maintainer__ = "JJ Brown"
__status__ = "development"

import matplotlib.pyplot as plt
import handle_command_line_IO
from abinit_data_types import parse_atoms, Experiment, Coordinate

def display_atoms_rhombus(atoms):
    """
    Displays the atoms's coordinates in a rhombus unit cell
    """
    xyz_unit = [atom.coord for atom in atoms]
    xyz_rhombus = [shear_to_rhombal_grid(coord).coordinate_array for coord in xyz_unit]
    (x_rhombus, y_rhombus) = ([coord[0] for coord in xyz_rhombus], \
                              [coord[1] for coord in xyz_rhombus])
    plt.axis('equal')
    plt.plot(x_rhombus, y_rhombus, 'ro',
             [0, 1, 1.5, 0.5, 0], [0, 0, (3**0.5)/2, (3**0.5)/2, 0], 'b--')
    plt.show()

def shear_to_rhombal_grid(coordinate):
    """Maps a Coordinate from the unit grid to a 60° unit-length rhombus"""
    point = coordinate.coordinate_array
    return Coordinate(coordinate_array=[point[0]+0.5*point[1], point[1]*(3**0.5)/2, point[2]], \
                      coordinate_system=coordinate.coordinate_system)

def main():
    """
    Displays the atoms from the meta attributes of the input experiment within a rhombal unit cell
    """
    with handle_command_line_IO.get_input_file(display_help_function) as input_file:
        experiment = Experiment.load_from_json_file(input_file)
        atoms = parse_atoms(experiment.meta['atoms'])
        display_atoms_rhombus(atoms)

def display_help_function():
    """
    displays usage information for this file
    """
    handle_command_line_IO.errprint(\
    	'Usage: [echo input_file.abinit.json | ] '+\
    	'python visualize_rhombus_cell.py [input_file.abinit.json]')

if __name__ == '__main__':
    main()
