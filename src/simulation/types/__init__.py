from .coordinates import Coordinates3D, CarthesianCoordinates, CylindricalCoordinates
from .vectors import (
    Vector3D,
    Array1D,
    Array2D
)
from .Piece import Piece, PieceDimensions

#============================================================

from typing import TypedDict, TYPE_CHECKING

from enum import Enum

if TYPE_CHECKING:
    from ..magnetism import PieceMagnet

type MagnetMap = (
    list[PieceMagnet[CarthesianCoordinates]] | 
    list[PieceMagnet[CylindricalCoordinates]]
)


class DipoleOrientation(Enum):
    UP = (0,0,1)
    DOWN = (0,0,-1)


Force = TypedDict(
    'Force',
    {
        'force_name': str,
        'force_vector': Vector3D,
        'body_point': Coordinates3D | None
    }
)