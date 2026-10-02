from enum import Enum
from typing import TypedDict

from numpy.typing import NDArray
from numpy import float64, ndarray, dtype, generic

type Point3D = tuple[float, float, float]

type _Vector3D[ScalarT: generic] = ndarray[tuple[int], dtype[ScalarT]]
type _Array1D[ScalarT: generic] = ndarray[tuple[int], dtype[ScalarT]]
type _Array2D[ScalarT: generic] = ndarray[tuple[int, int], dtype[ScalarT]]

type Vector3D = _Vector3D[float64]
type Array1D = _Array1D[float64]
type Array2D = _Array2D[float64]


PieceDimensions = TypedDict(
    'PieceDimensions',
    {
        'length': float,
        'width': float,
        'height': float
    }
)

Force = TypedDict(
    'Force',
    {
        'force_name': str,
        'force_vector': Vector3D,
    }
)

class DipoleOrientation(Enum):
    UP = (0,0,1)
    DOWN = (0,0,-1)