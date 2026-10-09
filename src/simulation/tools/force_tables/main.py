import json
from pathlib import Path
from typing import Any

import numpy as np

from ...magnetism.Magnet import Magnet
from ...types import (
    Vector3D,
    Array1D,
    CarthesianCoordinates,
)

BASE_DIR = Path(__file__).resolve().parent

def get_config_json(filename:str):
    filepath = BASE_DIR / 'configs' / filename

    with filepath.open(encoding='utf-8') as json_config_file:
        config = json.load(json_config_file)

    if not isinstance(config, dict):
        raise ImportError(f'Config is not a dictionary -> {config}')
    
    return config


def setup_configuration(config:dict[str,Any]):
    c_keys = list(config.keys())

    magnets = list(map(
        lambda key: Magnet(
            position=CarthesianCoordinates(x=0,y=0,z=0),
            radius=float(config[key]['radius']),
            thickness=float(config[key]['thickness']),
            magnetization=np.array(config[key]['magnetization'])
        ),
        filter(
            lambda key: key.startswith('magnet_'),
            c_keys
        )
    ))

    #temporary
    for magnet in magnets:
        magnet.set_magnet_map_in_carthesian_system(
            mapping=magnet.mapping_pieces_magnet(n_pieces=10**3)
        )

    grid = config['grid']
    output = config['output']

    dx_grid:Array1D
    dy_grid:Array1D
    dz_grid:Array1D

    dx_grid, dy_grid, dz_grid = (
                        np.linspace(
                            grid['dx']['min'],
                            grid['dx']['max'],
                            grid['dx']['count']
                        ),
                        np.linspace(
                            grid['dy']['min'],
                            grid['dy']['max'],
                            grid['dy']['count']
                        ),
                        np.linspace(
                            grid['dz']['min'],
                            grid['dz']['max'],
                            grid['dz']['count']
                        )
                        )

    grid_forces = np.empty((
        grid['dx']['count'],
        grid['dy']['count'],
        grid['dz']['count'],
        3,
    )) #implemet typing in this shit

    return {
        'grid_positions': (dx_grid, dy_grid, dz_grid),
        'grid_forces': grid_forces,
        'output': output,
        'magnets': magnets
    }


#WORK FOR ONLY 2 MAGNETS
def populate_force_grid(grid:tuple[Array1D, Array1D, Array1D], grid_forces:Any, magnets:list[Magnet]) -> Any:
    x_grid, y_grid, z_grid = grid

    for k, dz in enumerate(z_grid):
        for j, dy in enumerate(y_grid):
            for i, dx in enumerate(x_grid):
                grid_forces[i][j][k] = force_in_grid(
                    position=np.array((dx, dy, dz)),
                    magnets=magnets
                )

    return grid_forces


#WORK FOR ONLY 2 MAGNETS
def force_in_grid(position, magnets:list[Magnet]) -> Vector3D:
    magnet, magnet_fixed = magnets
    e_x, e_y, e_z = (
                     np.array((1,0,0)),
                     np.array((0,1,0)),
                     np.array((0,0,1))
                    )

    magnet.position = position
    vector_force = magnet.magnetic_force_with(magnet=magnet_fixed)

    return (
        np.dot(vector_force[0], e_x) +
        np.dot(vector_force[1], e_y) +
        np.dot(vector_force[2], e_z)
    )


def save_force_table(
    force_table_id: str,
    grid_positions: tuple[Array1D, Array1D, Array1D],
    grid_forces: Any,
) -> Path:

    filepath = BASE_DIR / 'data' / f'{force_table_id}.npz'

    x_grid, y_grid, z_grid = grid_positions

    with filepath.open('xb') as file:
        np.savez_compressed(
            file,
            dx_grid=x_grid,
            dy_grid=y_grid,
            dz_grid=z_grid,
            grid_forces=grid_forces
        )

    return filepath


def load_force_table(force_table_id: str):
    filepath = BASE_DIR / 'data' / f'{force_table_id}.npz'

    with np.load(filepath, allow_pickle=False) as force_table_file:
        force_table = {
            'dx_grid': force_table_file['dx_grid'],
            'dy_grid': force_table_file['dy_grid'],
            'dz_grid': force_table_file['dz_grid'],
            'grid_forces': force_table_file['grid_forces']
        }

    print('\x1b[33m', len(force_table['grid_forces'].ravel()), '\x1b[0m')

    return force_table


def main2():
    config_file = input('Insert Configuration file... ')

    filepath = BASE_DIR / 'configs' / config_file
    if not filepath.exists():
        raise FileNotFoundError(f'The file {config_file} is not found in {(BASE_DIR / 'configs').absolute()}')

    config = setup_configuration(get_config_json(filename=config_file))

    grid_positions = config['grid_positions']
    grid_forces = config['grid_forces']
    output = config['output']
    magnets = config['magnets']

    grid_forces = populate_force_grid(
        grid=grid_positions,
        grid_forces=grid_forces,
        magnets=magnets
    )

    save_force_table(
        force_table_id=output,
        grid_positions=grid_positions,
        grid_forces=grid_forces
    )

    print(load_force_table(force_table_id=output))

