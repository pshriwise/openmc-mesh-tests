#!/usr/bin/env python

import numpy as np
import openmc

from properties import model
from properties import _HEIGHT, _PITCH

def create_csg_model(materials):

    fuel_mat = materials[0]

    # create a simple csg cell
    x_min = openmc.XPlane(-0.5 * _PITCH, boundary_type='reflective')
    x_max = openmc.XPlane(0.5 * _PITCH, boundary_type='reflective')
    y_min = openmc.YPlane(-0.5 * _PITCH, boundary_type='reflective')
    y_max = openmc.YPlane(0.5 * _PITCH, boundary_type='reflective')
    z_min = openmc.ZPlane(-0.5 * _HEIGHT, boundary_type='vacuum')
    z_max = openmc.ZPlane(0.5 * _HEIGHT, boundary_type='vacuum')
    box = +x_min & -x_max & +y_min & -y_max & +z_min & -z_max

    inner_z_cyl = openmc.ZCylinder(r=0.5)
    outer_z_cyl = openmc.ZCylinder(r=1.0)

    x_mid = openmc.XPlane(0.0)
    y_mid = openmc.YPlane(0.0)

    fuel_cells = []
    q1_region = +x_mid & -x_max & +y_mid & -y_max & +z_min & -z_max
    q1_inner = openmc.Cell(fill=fuel_mat, region=q1_region & -inner_z_cyl)
    q1_outer = openmc.Cell(fill=fuel_mat, region=q1_region & +inner_z_cyl & -outer_z_cyl)
    fuel_cells += [q1_inner, q1_outer]

    q2_region = +x_min & -x_mid & +y_mid & -y_max & +z_min & -z_max
    q2_inner = openmc.Cell(fill=fuel_mat, region=q2_region & -inner_z_cyl)
    q2_outer = openmc.Cell(fill=fuel_mat, region=q2_region & +inner_z_cyl & -outer_z_cyl)
    fuel_cells += [q2_inner, q2_outer]

    q3_region = +x_min & -x_mid & +y_min & -y_mid & +z_min & -z_max
    q3_inner = openmc.Cell(fill=fuel_mat, region=q3_region & -inner_z_cyl)
    q3_outer = openmc.Cell(fill=fuel_mat, region=q3_region & +inner_z_cyl & -outer_z_cyl)
    fuel_cells += [q3_inner, q3_outer]

    q4_region = +x_mid & -x_max & +y_min & -y_mid & +z_min & -z_max
    q4_inner = openmc.Cell(fill=fuel_mat, region=q4_region & -inner_z_cyl)
    q4_outer = openmc.Cell(fill=fuel_mat, region=q4_region & +inner_z_cyl & -outer_z_cyl)
    fuel_cells += [q4_inner, q4_outer]

    outer_region = box & +outer_z_cyl
    outer = openmc.Cell(fill=materials[3], region=outer_region)

    root_univ = openmc.Universe(cells=fuel_cells + [outer])

    geom = openmc.Geometry(root_univ)

    return geom


def create_tallies(cells):

    # create a cylindrical mesh that matches the
    mesh = openmc.CylindricalMesh()
    mesh.r_grid = np.linspace(0.0, 1.0, 3)
    mesh.z_grid = np.linspace(-0.5 * _HEIGHT, 0.5 * _HEIGHT, 2)
    mesh.phi_grid = np.linspace(0, 2 * np.pi, 5)

    mesh_tally = openmc.Tally()
    mesh_tally.filters = [openmc.MeshFilter(mesh)]
    mesh_tally.scores = ['flux']

    cell_tally = openmc.Tally()
    cell_ids = [c.id for c in cells]
    cell_tally.filters = [openmc.CellFilter(cell_ids)]
    cell_tally.scores = ['flux']

    openmc.Tallies([mesh_tally, cell_tally]).export_to_xml()


def cells_by_material(geom, material):
    return [c for c in geom.get_all_cells().values() if c.fill == material]


def test_cylindrical_mesh():
    model.geometry = create_csg_model(model.materials)
    fuel_cells = cells_by_material(model.geometry, model.materials[0])
    create_tallies(fuel_cells)