from math import (
    pi,
    sqrt
)

import numpy as np

from .types import Vector3D, PieceDimensions
from .PieceMagnet import PieceMagnet

class Magnet:
    N_MAP_PIECES = 100

    # piece_dimensions:PieceDimensions
    magnet_map:list[PieceMagnet]

    def __init__(
            self,
            radius: float,
            thickness: float,
            magnetization: Vector3D,
            position: Vector3D
    ) -> None:

        if position[2] != 0:
            raise RuntimeError()

        self.position = position
        self.radius = radius
        self.thickness = thickness
        self.magnetization = magnetization
        self.magnet_volume = Magnet.volume(self)


    def volume(self):
        r, h = self.radius, self.thickness
        return pi * (r) * (r) * (h)


    @staticmethod
    def get_piece_dimensions(volume:float) -> PieceDimensions:
        # IMPLEMENT PIECES FORMATS
        # NOW USES A CUBE FORMAT

        return {
            'length': (volume)**(1/3),
            'width': (volume)**(1/3),
            'height': (volume)**(1/3),
        }
    

    def set_magnet_map(self, mapping:list[Vector3D], volume_by_piece:float) -> None:
        self.magnet_map = list(map(
            lambda piece_position: PieceMagnet(
                position=piece_position,
                dimensions=Magnet.get_piece_dimensions(volume_by_piece),
                magnetization=self.magnetization
            ),
            mapping
        ))


    def magnetic_force_with(self, magnet:Magnet) -> Vector3D:

        magnetic_force_total = np.zeros(3)
        for piece in self.magnet_map:
            for target_piece in magnet.magnet_map:
                piece.position += self.position
                target_piece.position += magnet.position

                magnetic_force_total += piece.force_with(dipole=target_piece)

        return magnetic_force_total


    def interaction_energy_with(self, magnet:Magnet) -> float:

        interaction_total_energy = 0.0
        for piece in self.magnet_map:
            for target_piece in magnet.magnet_map:
                interaction_total_energy += piece.interaction_energy_with(dipole=target_piece)

        return interaction_total_energy

    
    def mapping_pieces_magnet(self, n_pieces:int | None = None) -> list:
        n_pieces = n_pieces or self.N_MAP_PIECES
        self.piece_dimensions = Magnet.get_piece_dimensions(self.magnet_volume / n_pieces)

        l, w, h = self.piece_dimensions.values()
        center_magnet = (0, 0, 0)
        pieces = list(
            self._traverse_z_direction(position=center_magnet)
        )

        volume = sum(
            map(
                lambda piece: l*w*h,
                pieces
            )
        )

        print(f'len of pieces list {len(pieces)}')

        err_vol = (abs(volume - self.magnet_volume)) / self.magnet_volume
        if round(err_vol, 3) > 1.005:
            raise ValueError(f'Volume aproximado excede ao volume do ima; volume_aprox:{volume}, volume_teorico:{self.magnet_volume}, {err_vol}')

        return pieces

        
    def _traverse_z_direction(self, position:tuple[float, float, float]):
        piece = position
        simetric_piece = piece

        l_z = self.thickness

        dz = 0
        z_max = l_z / 2

        pieces:set[tuple[float,float,float]] = set()
        while piece[2] + dz < z_max:
            piece, simetric_piece = (
                piece[0],
                piece[1],
                piece[2] + dz
            ), (
                simetric_piece[0],
                simetric_piece[1],
                simetric_piece[2] - dz
            )
        
            get_x = self._traverse_x_direction

            piece_x_set = get_x(position=piece)
            simetric_piece_x_set = get_x(position=simetric_piece)

            additional_pieces_set = piece_x_set | simetric_piece_x_set
            pieces = pieces | additional_pieces_set

            dz = self.piece_dimensions['height']

        return pieces


    def _traverse_x_direction(self, position:tuple[float,float,float]) -> set[tuple[float, float, float]]:
        piece = position
        simetric_piece = piece

        dy = self.piece_dimensions['width']
        dx, x_max = 0, self.radius

        pieces: set[tuple[float,float,float]] = set()
        while piece[0] + dx < x_max:
            piece, simetric_piece = (
                piece[0] + dx,
                piece[1],
                piece[2]
            ), (
                simetric_piece[0] - dx,
                simetric_piece[1],
                simetric_piece[2]
            )
        
            get_y = self._traverse_y_direction
        
            piece_y_set = get_y(position=piece)
            simetric_piece_y_set = get_y(position=simetric_piece)
        
            additional_pieces_set = piece_y_set | simetric_piece_y_set
            pieces = pieces | additional_pieces_set
        
            dx = self.piece_dimensions['length']

        return pieces


    def _traverse_y_direction(self, position:tuple[float, float, float]) -> set[tuple[float,float,float]]:
        piece = position
        simetric_piece = piece

        dy = 0
        y_max = abs(sqrt(self.radius**2 - piece[0]**2))

        pieces:list[tuple[float,float,float]] = []
        while piece[1] + dy < y_max: # we use the simetric of axis y; always starting in axis for simetry
            (piece, simetric_piece) = (
                piece[0],
                piece[1] + dy,
                piece[2]
            ), (
                simetric_piece[0],
                simetric_piece[1] - dy,
                simetric_piece[2]
            )
        
            pieces.extend([piece, simetric_piece])
            dy = self.piece_dimensions['width']

        return set(pieces)