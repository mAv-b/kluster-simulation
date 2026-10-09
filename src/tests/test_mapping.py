from math import pi

import pytest
import numpy as np

from simulation.magnetism import Magnet
from simulation.types import (
    CarthesianCoordinates,
    Vector3D,
)

class TestMagnetMappingByCylindrical:

    @pytest.fixture(params=[
        0.005,
        0.010,
        0.020,
    ])
    def radius(self, request) -> float:
        return float(request.param)


    @pytest.fixture(params=[
        0.001,
        0.005,
        0.010
    ])
    def thickness(self, request) -> float:
        return float(request.param)


    @pytest.fixture(params=[
        (0.0, 0.0, 400_000.0),
        (0.0, 0.0, 800_000.0),
        (0.0, 0.0, -800_000.0),
    ])
    def magnetization(self, request) -> Vector3D:
        return np.array(request.param)


    @pytest.fixture(params=[
        (0.0, 0.0, 0.0),
        (0.03, 0.02, 0.0),
        (-0.02, -0.03, 0.0),
    ])
    def position(self, request) -> CarthesianCoordinates:
        return CarthesianCoordinates(*request.param)


    @pytest.fixture
    def magnet(self, radius, thickness, magnetization, position):
        return Magnet(
            radius=radius,
            thickness=thickness, 
            magnetization=magnetization,
            position=position
        )

    
    @pytest.mark.parametrize('n_pieces', [
        10**(i) for i in range(1, 5)
    ])
    def test_mapping_volume(self, magnet, n_pieces):
        mapping_magnet = magnet.mapping_pieces_magnet_by_cilindral_method(n_pieces=n_pieces)
        magnet.set_magnet_map_in_carthesian_system(mapping_magnet)

        volume = sum(
            map(
                lambda magnet_piece: magnet_piece.piece.volume,
                magnet.magnet_map
            )
        )

        expected_volume = pi * magnet.radius * magnet.radius * magnet.thickness

        rel_error = (
            (volume - expected_volume) / expected_volume
        )

        print(f"Expected volume: {expected_volume:.10e} m³")
        print(f"Obtained volume: {volume:.10e} m³")
        print(f"Relative error:  {rel_error:+.3%}")

        assert expected_volume == pytest.approx(
            volume,
            rel=1e-2,
            abs=1e-12
        )