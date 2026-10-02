from pathlib import Path

from scipy.interpolate import RegularGridInterpolator

from ..types import Vector3D

from .force_tables.main import (
    load_force_table
)

class Interpolation:
    def __init__(
        self,
        filepath:Path,
    ) -> None:

        self.filepath = filepath
        if not self.filepath.exists():
            raise FileNotFoundError()
        elif self.filepath.suffix != '.npz' or self.filepath.parent.parts[-1] != 'data':
            raise RuntimeError()

        self.force_table = load_force_table(
            self.filepath.name
        )


    def init_interpolation(self) -> RegularGridInterpolator:
        dx_grid = self.force_table['dx_grid']
        dy_grid = self.force_table['dy_grid']
        dz_grid = self.force_table['dz_grid']

        grid_forces = self.force_table['grid_forces']

        self.interpolator = RegularGridInterpolator(
            (dx_grid, dy_grid, dz_grid),
            grid_forces,
            method='linear',
            bounds_error=True
        )

        return self.interpolator


    def force_relative_at(self, rel_position:Vector3D) -> Vector3D:
        if self.interpolator is None:
            raise KeyError('interpolator not definied')

        return self.interpolator(
            [
                rel_position,
            ]
        )[0]

        
