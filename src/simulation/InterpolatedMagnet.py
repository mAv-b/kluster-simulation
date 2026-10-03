from .Magnet import Magnet
from .types import Vector3D
from .tools.Interpolation import Interpolation

class InterpolatedMagnet(Magnet):
    _magnetic_force: Vector3D

    def __init__(
        self,
        radius: float, 
        thickness: float, 
        magnetization: Vector3D, 
        position: Vector3D,
        interpolation: Interpolation
    ) -> None:

        self.interpolation = interpolation
        
        super().__init__(radius, thickness, magnetization, position)


    @property
    def magnetic_force(self) -> Vector3D:
        return self._magnetic_force


    @magnetic_force.setter
    def magnetic_force(self) -> None:
        self._magnetic_force = self.interpolation.force_relative_at(rel_position=self.position)