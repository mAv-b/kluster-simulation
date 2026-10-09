import pytest
import numpy as np

from simulation.types import (
    CarthesianCoordinates,
)
from simulation.magnetism import PointDipole

_vector3d = np.array

class TestPointDipole:

    def setup_method(self):
        self.dipole = PointDipole(
            position=CarthesianCoordinates(*(0,0,0)),
            magnetic_moment=_vector3d((0,0,1))
        )


    @pytest.mark.parametrize('position, expected_magnetic_field', [
        (CarthesianCoordinates(x=0, y=0, z=1), _vector3d([0, 0, 2e-7])),
        (CarthesianCoordinates(x=0,y=0,z=-1), _vector3d([0, 0, 2e-7])),
        (CarthesianCoordinates(x=1, y=0, z=0), _vector3d([0, 0, -1e-7])),
        (CarthesianCoordinates(x=0, y=1, z=0), _vector3d([0, 0, -1e-7])),
        (CarthesianCoordinates(x=-1, y=0, z=0), _vector3d([0, 0, -1e-7])),
        (CarthesianCoordinates(x=0, y=0, z=2), _vector3d([0, 0, 2.5e-8])),
        (CarthesianCoordinates(x=2, y=0, z=0), _vector3d([0, 0, -1.25e-8])),
        (CarthesianCoordinates(x=1, y=0, z=1), _vector3d([5.3033e-8, 0, 1.7678e-8])),
        (CarthesianCoordinates(x=0, y=1, z=1), _vector3d([0, 5.3033e-8, 1.7678e-8])),
        (CarthesianCoordinates(x=-1, y=0, z=1), _vector3d([-5.3033e-8, 0, 1.7678e-8]))
        
    ])
    def test_magnetic_field_at(self, position, expected_magnetic_field):
        magnetic_field = self.dipole.magnetic_field_at(position)

        np.testing.assert_allclose(
            magnetic_field,
            expected_magnetic_field,
            rtol=1e-4,
            atol=1e-15
        )

    