from math import (
    pi,
    cbrt,
    ceil
)

import numpy as np

from ..types import (
    Vector3D,
    CylindricalCoordinates,
    Coordinates3D,
    MagnetMap
)
from ..types.Piece import Piece
from .PieceMagnet import PieceMagnet

class Magnet:
    _position: Coordinates3D
    magnet_map:MagnetMap

    def __init__(
            self,
            radius: float,
            thickness: float,
            magnetization: Vector3D,
            position: Coordinates3D
    ) -> None:

        if position.to_vector3D()[2] != 0:
            raise RuntimeError()

        self.position = position
        self.radius = radius
        self.thickness = thickness
        self.magnetization = magnetization
        self.magnet_volume = pi * radius * radius * thickness


    @property
    def position(self) -> Coordinates3D:
        return self._position


    @position.setter
    def position(self, position: Coordinates3D) -> None:
        self._position = position

        if hasattr(self, "magnet_map"):
            for piece in self.magnet_map:
                piece.position = self.position + piece.piece.relative_position


    def magnetic_force_with(self, magnet:Magnet) -> Vector3D:

        magnetic_force_total = np.zeros(3)
        for piece in self.magnet_map:
            for target_piece in magnet.magnet_map:
                magnetic_force_total += piece.force_with(dipole=target_piece)

        return magnetic_force_total


    def interaction_energy_with(self, magnet:Magnet) -> float:

        interaction_total_energy = 0.0
        for piece in self.magnet_map:
            for target_piece in magnet.magnet_map:
                interaction_total_energy += piece.interaction_energy_with(dipole=target_piece)

        return interaction_total_energy


    def set_magnet_map_in_carthesian_system(self, mapping:list[Piece[CylindricalCoordinates]]) -> None:
        carthesian_pieces = list(map(
            lambda piece: Piece(
                relative_position=piece.relative_position.cylindrical_2_carthesian(),
                volume=piece.volume
            ),
            mapping
        ))

        for piece in carthesian_pieces:
            piece.position = self.position


        self.magnet_map = list(
            map(
                lambda piece: PieceMagnet(
                    piece=piece,
                    magnetization=self.magnetization
                ),
                carthesian_pieces
            )
        )


    def mapping_pieces_magnet_by_cilindral_method(self, n_pieces:int) -> list[Piece[CylindricalCoordinates]]:
        pieces_step_len = cbrt(n_pieces)
        center_magnet = CylindricalCoordinates(*np.zeros(3))

        return list(
            self._discretize_along_axial_axis(
                position=center_magnet,
                axis_step=ceil(pieces_step_len)
            )
        )


    def _discretize_along_axial_axis(self, position:CylindricalCoordinates, axis_step:int) -> set[Piece[CylindricalCoordinates]]:
        z_max = self.thickness / 2

        axial_axis = np.linspace(
            position.z - z_max, position.z + z_max, axis_step, endpoint=False)

        step_len = self.thickness / axis_step

        axial_pieces:set[Piece[CylindricalCoordinates]] = set()
        for _z in axial_axis:
            _position = CylindricalCoordinates(
                r=position.r,
                theta=position.theta,
                z=_z + (step_len / 2)
            )

            pieces_cross_azimuthal_axis = self._discretize_along_azimuthal_axis(
                position=_position, axis_step=axis_step)

            axial_pieces |= pieces_cross_azimuthal_axis

        return axial_pieces


    def _discretize_along_azimuthal_axis(self, position:CylindricalCoordinates, axis_step:int) -> set[Piece[CylindricalCoordinates]]:
        theta_max = 2 * pi

        azimuthal_axis = np.linspace(
            position.theta, position.theta + theta_max, axis_step, endpoint=False
        )

        azimuthal_pieces:set[Piece[CylindricalCoordinates]] = set()
        for _theta in azimuthal_axis:
            _position = CylindricalCoordinates(
                r=position.r,
                theta=_theta,
                z=position.z
            )

            pieces_cross_radial_axis = self._discretize_along_radial_axis(
                position=_position, axis_step=axis_step)

            azimuthal_pieces |= pieces_cross_radial_axis

        return azimuthal_pieces


    def _discretize_along_radial_axis(self, position:CylindricalCoordinates, axis_step:int) -> set[Piece[CylindricalCoordinates]]:
        r_max = self.radius

        radial_axis = np.linspace(
            position.r, position.r + r_max, axis_step, endpoint=False
        )

        step_len = self.radius / axis_step

        radial_pieces:set[Piece[CylindricalCoordinates]] = set()
        for _r in radial_axis:
            _position = CylindricalCoordinates(
                r=_r + (step_len / 2),
                theta=position.theta,
                z=position.z
            )

            d_r = step_len
            d_theta = 2 * pi / axis_step
            d_z = self.thickness / axis_step

            exterior_radius, interior_radius = _r + d_r, _r

            piece_volume = ((exterior_radius**2 - interior_radius**2) / 2) * d_theta * d_z

            radial_pieces.add(
                Piece(
                    relative_position=_position,
                    volume=piece_volume
                )
            )

        return radial_pieces


    # def mapping_pieces_magnet_by_cilindral_method(self, n_pieces:int) -> list[Piece[CylindricalCoordinates]]:

    #     differential_length = cbrt(
    #         (2 * pi * self.radius * self.radius * self.thickness) / n_pieces
    #     )

    #     center_magnet:CarthesianCoordinates = CarthesianCoordinates(*np.zeros(3))
    #     cylindrical_coord_pieces = list(
    #         self._discretize_along_axial_axis(
    #             position=center_magnet.carthesian_2_cylindrical(),
    #             d_z=CylindricalCoordinates(r=0, theta=0, z=differential_length)
    #         )
    #     )

    #     return cylindrical_coord_pieces


    # def _discretize_along_axial_axis(self, d_z:CylindricalCoordinates, position:CylindricalCoordinates) -> set[Piece[CylindricalCoordinates]]:

    #     d_z_vector = CylindricalCoordinates(r=0, theta=0, z=0)
    #     piece = position
    #     simetric_piece = position

    #     z_max = self.thickness / 2
    #     z_disk_pieces:set[Piece[CylindricalCoordinates]] = set()
        
    #     while piece.z + d_z_vector.z < z_max:
    #         piece = piece + d_z_vector
    #         simetric_piece = simetric_piece - d_z_vector

    #         d_theta = CylindricalCoordinates(r=0, theta=d_z.z, z=0)

    #         piece_cross_azimuthal_direction = self._discretize_along_azimuthal_axis(
    #             d_theta=d_theta, position=piece)
    #         simetric_piece_cross_azimuthal_direction = self._discretize_along_azimuthal_axis(
    #             d_theta=d_theta, position=simetric_piece)

    #         disk_pieces = piece_cross_azimuthal_direction | simetric_piece_cross_azimuthal_direction
    #         z_disk_pieces |= disk_pieces
            
    #         d_z_vector = d_z

    #     return z_disk_pieces
    

    # def _discretize_along_azimuthal_axis(self, d_theta:CylindricalCoordinates, position:CylindricalCoordinates) -> set[Piece[CylindricalCoordinates]]:
    #     piece = position

    #     azimuthal_vector = CylindricalCoordinates(r=0, theta=0, z=0)
    #     max_azimuthal_angle = 2*pi

    #     azimuthal_pieces:set[Piece[CylindricalCoordinates]] = set()
    #     while piece.theta + azimuthal_vector.theta <= max_azimuthal_angle:
    #         piece += azimuthal_vector

    #         d_r = CylindricalCoordinates(r=d_theta.theta, theta=0, z=0)

    #         pieces_cross_radial_direction = self._discretize_along_radial_axis(
    #             d_r=d_r, position=piece)

    #         azimuthal_pieces |= pieces_cross_radial_direction
    #         azimuthal_vector = d_theta
    #         print('\1xb[33m', piece.theta + azimuthal_vector.theta, '\1xb[0m')

    #     p = any(
    #         piece.relative_position.theta > max_azimuthal_angle for piece in azimuthal_pieces
    #     )
    #     print(p)
    #     if p:
    #         print(f'Passou do angulo maximo o mapeamento {p}, esperado: {max_azimuthal_angle}')

    #     return azimuthal_pieces


    # def _discretize_along_radial_axis(self, d_r:CylindricalCoordinates, position:CylindricalCoordinates) -> set[Piece[CylindricalCoordinates]]:
    #     piece_pos = position

    #     d_r_vector = CylindricalCoordinates(r=0, theta=0, z=0)
    #     max_r = self.radius

    #     radial_pieces:set[Piece[CylindricalCoordinates]] = set()
    #     while piece_pos.r + d_r_vector.r <= max_r:
    #         piece_pos += d_r_vector

    #         _T_d_theta, _T_d_z = d_r.norm(), d_r.norm()
    #         exterior_radius, interior_radius = (piece_pos.r,
    #                                             piece_pos.r - d_r_vector.r)
            
    #         piece_volume = ( (exterior_radius**2 - interior_radius**2) / 2 ) * _T_d_theta * _T_d_z

    #         piece = Piece(
    #             relative_position=piece_pos, volume=piece_volume)
    #         piece.position = self.position

    #         radial_pieces.add(piece)
    #         d_r_vector = d_r

    #     #TEMP CHECK
    #     p = any(
    #         piece.relative_position.r > max_r for piece in radial_pieces
    #     )
        
    #     if p:
    #         print(f'passou o eixo radial aqui {p}; esperado: {max_r}')

    #     #print(len(radial_pieces))
    #     return radial_pieces


    # def mapping_pieces_magnet(self, n_pieces:int | None = None) -> list:
    #     n_pieces = n_pieces or self.N_MAP_PIECES
    #     self.piece_dimensions = Magnet.get_piece_dimensions(self.magnet_volume / n_pieces)

    #     l, w, h = self.piece_dimensions.values()
    #     center_magnet = (0, 0, 0)
    #     pieces = list(
    #         self._traverse_z_direction(position=center_magnet)
    #     )

    #     volume = sum(
    #         map(
    #             lambda piece: l*w*h, # type: ignore
    #             pieces
    #         )
    #     )

    #     err_vol = (abs(volume - self.magnet_volume)) / self.magnet_volume
    #     if round(err_vol, 3) > 1.005:
    #         raise ValueError(f'Volume aproximado excede ao volume do ima; volume_aprox:{volume}, volume_teorico:{self.magnet_volume}, {err_vol}')

    #     return pieces

        
    # def _traverse_z_direction(self, position:tuple[float, float, float]):
    #     piece = position
    #     simetric_piece = piece

    #     l_z = self.thickness

    #     dz = 0
    #     z_max = l_z / 2

    #     pieces:set[tuple[float,float,float]] = set()
    #     while piece[2] + dz < z_max:
    #         piece, simetric_piece = (
    #             piece[0],
    #             piece[1],
    #             piece[2] + dz
    #         ), (
    #             simetric_piece[0],
    #             simetric_piece[1],
    #             simetric_piece[2] - dz
    #         )
        
    #         get_x = self._traverse_x_direction

    #         piece_x_set = get_x(position=piece)
    #         simetric_piece_x_set = get_x(position=simetric_piece)

    #         additional_pieces_set = piece_x_set | simetric_piece_x_set
    #         pieces = pieces | additional_pieces_set

    #         dz = self.piece_dimensions['height']

    #     return pieces


    # def _traverse_x_direction(self, position:tuple[float,float,float]) -> set[tuple[float, float, float]]:
    #     piece = position
    #     simetric_piece = piece

    #     dy = self.piece_dimensions['width']
    #     dx, x_max = 0, self.radius

    #     pieces: set[tuple[float,float,float]] = set()
    #     while piece[0] + dx < x_max:
    #         piece, simetric_piece = (
    #             piece[0] + dx,
    #             piece[1],
    #             piece[2]
    #         ), (
    #             simetric_piece[0] - dx,
    #             simetric_piece[1],
    #             simetric_piece[2]
    #         )
        
    #         get_y = self._traverse_y_direction
        
    #         piece_y_set = get_y(position=piece)
    #         simetric_piece_y_set = get_y(position=simetric_piece)
        
    #         additional_pieces_set = piece_y_set | simetric_piece_y_set
    #         pieces = pieces | additional_pieces_set
        
    #         dx = self.piece_dimensions['length']

    #     return pieces


    # def _traverse_y_direction(self, position:tuple[float, float, float]) -> set[tuple[float,float,float]]:
    #     piece = position
    #     simetric_piece = piece

    #     dy = 0
    #     y_max = abs(sqrt(self.radius**2 - piece[0]**2))

    #     pieces:list[tuple[float,float,float]] = []
    #     while piece[1] + dy < y_max: # we use the simetric of axis y; always starting in axis for simetry
    #         (piece, simetric_piece) = (
    #             piece[0],
    #             piece[1] + dy,
    #             piece[2]
    #         ), (
    #             simetric_piece[0],
    #             simetric_piece[1] - dy,
    #             simetric_piece[2]
    #         )
        
    #         pieces.extend([piece, simetric_piece])
    #         dy = self.piece_dimensions['width']

    #     return set(pieces)