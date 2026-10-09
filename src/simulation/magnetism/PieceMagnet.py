from .PointDipole import PointDipole
from ..types import Vector3D, Coordinates3D
from ..types.Piece import Piece

#TODO check for a possible multiple inheirint...
#FIXME Having a Piece property, duplicate position property, is redundant???
class PieceMagnet[CoordT: Coordinates3D](PointDipole):
    #FIXME THIS IS USING??? i forgot
    # _absolute_position: Coordinates3D 

    def __init__(
        self,
        piece:Piece[CoordT],
        magnetization: Vector3D,
    ) -> None:

        self.piece = piece
        self.magnetization = magnetization

        if not hasattr(self.piece, 'position'):
            raise AttributeError(f'{self.piece.__str__} does not have a absolute position definied')

        super().__init__(
            piece.position,
            magnetic_moment=self.magnetization * self.piece.volume
        )
