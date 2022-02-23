from math import log10

import numpy as np
import openmc

###############################################################################
# Geometric parameters

_HEIGHT = 50  # cm
_PITCH = 3.0  # cm
_FUEL_OR = 1.0  # cm

###############################################################################
# Create materials for the problem

uo2 = openmc.Material(name='UO2 fuel at 2.4% wt enrichment')
uo2.set_density('g/cm3', 10.29769)
uo2.add_element('U', 1., enrichment=2.4)
uo2.add_element('O', 2.)

helium = openmc.Material(name='Helium for gap')
helium.set_density('g/cm3', 0.001598)
helium.add_element('He', 2.4044e-4)

zircaloy = openmc.Material(name='Zircaloy 4')
zircaloy.set_density('g/cm3', 6.55)
zircaloy.add_element('Sn', 0.014  , 'wo')
zircaloy.add_element('Fe', 0.00165, 'wo')
zircaloy.add_element('Cr', 0.001  , 'wo')
zircaloy.add_element('Zr', 0.98335, 'wo')

borated_water = openmc.Material(name='Borated water')
borated_water.set_density('g/cm3', 0.740582)
borated_water.add_element('B', 4.0e-5)
borated_water.add_element('H', 5.0e-2)
borated_water.add_element('O', 2.4e-2)
borated_water.add_s_alpha_beta('c_H_in_H2O')

# Collect the materials together and export to XML
materials = openmc.Materials([uo2, helium, zircaloy, borated_water])

###############################################################################
# Define problem settings

# Indicate how many particles to run
settings = openmc.Settings()
settings.batches = 100
settings.inactive = 10
settings.particles = 1000

# Create an initial uniform spatial source distribution over fissionable zones
lower_left = (-_PITCH/2, -_PITCH/2, -1)
upper_right = (_PITCH/2, _PITCH/2, 1)
uniform_dist = openmc.stats.Box(lower_left, upper_right, only_fissionable=True)
settings.source = openmc.source.Source(space=uniform_dist)

# For source convergence checks, add a mesh that can be used to calculate the
# Shannon entropy
entropy_mesh = openmc.RegularMesh()
entropy_mesh.lower_left = (-_FUEL_OR, -_FUEL_OR)
entropy_mesh.upper_right = (_FUEL_OR, _FUEL_OR)
entropy_mesh.dimension = (10, 10)
settings.entropy_mesh = entropy_mesh

model = openmc.Model(materials=materials, settings=settings)