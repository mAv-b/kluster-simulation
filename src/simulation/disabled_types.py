from math import hypot, atan2, cos, sin
from enum import Enum
from typing import TypedDict, NamedTuple, Protocol, Self

from numpy.typing import NDArray
from numpy import float64, ndarray, dtype, generic
import numpy as np

class Coordinates3D(Protocol):
    def to_vector3D(self) -> Vector3D:
        ...

    def norm(self) -> float:
        ...

    def __add__(self, value) -> Self:
        ...

    def __sub__(self, value) -> Self:
        ...


class CarthesianCoordinates(NamedTuple):
    x:float
    y:float
    z:float

    def carthesian_2_cylindrical(self) -> CylindricalCoordinates:
        return CylindricalCoordinates(
            r=hypot(self.x, self.y),
            theta=atan2(self.y, self.x),
            z=self.z
        )


    def to_vector3D(self) -> Vector3D:
        return np.array([self.x, self.y, self.z])


    def norm(self) -> float:
        return np.linalg.norm(self.to_vector3D())


    def __add__(self, value: object) -> Self:
        if not isinstance(value, CarthesianCoordinates):
            return NotImplemented

        return type(self)(
             *(self.to_vector3D() + value.to_vector3D())
        )


    def __sub__(self, value: object) -> Self:
        if not isinstance(value, CarthesianCoordinates):
            return NotImplemented

        return type(self)(
            *(self.to_vector3D() - value.to_vector3D())
        )


class CylindricalCoordinates(NamedTuple):
    r: float
    theta: float
    z: float

    def cylindrical_2_carthesian(self) -> CarthesianCoordinates:
        return CarthesianCoordinates(
            x=self.r * cos(self.theta),
            y=self.r * sin(self.theta),
            z=self.z
        )


    def to_vector3D(self) -> Vector3D:
        return self.cylindrical_2_carthesian().to_vector3D()


    def norm(self) -> float:
        return self.cylindrical_2_carthesian().norm()
    

    def __add__(self, value: object) -> Self:
        if not isinstance(value, CylindricalCoordinates):
            return NotImplemented

        return type(self)(
            r=self.r + value.r,
            theta=self.theta + value.theta,
            z=self.z + value.z
        )


    def __sub__(self, value: object) -> Self:
        if not isinstance(value, CylindricalCoordinates):
            return NotImplemented

        return type(self)(
            r=self.r - value.r,
            theta=self.theta - value.theta,
            z=self.z - value.z
        )
    

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
        'body_point': Coordinates3D | None
    }
)

class DipoleOrientation(Enum):
    UP = (0,0,1)
    DOWN = (0,0,-1)