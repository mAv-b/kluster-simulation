from .PointDipole import PointDipole
from .types import Vector3D, PieceDimensions

class PieceMagnet(PointDipole):
    def __init__(
        self,
        position: Vector3D,
        dimensions: PieceDimensions,
        magnetization: Vector3D
    ) -> None:

        self.dimensions = dimensions
        self.magnetization = magnetization

        l, w, h = (self.dimensions['length'], 
                   self.dimensions['width'], 
                   self.dimensions['height'])
        self.volume = l * w * h

        super().__init__(
            position,
            magnetic_moment=self.magnetization * self.volume
        )
