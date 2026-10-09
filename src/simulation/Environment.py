from .types import Vector3D, Force
from .magnetism.DynamicMagnet import DynamicMagnet

class Environment:
    def __init__(self) -> None:
        pass


    def magnetic_forces_on(self, magnet: DynamicMagnet) -> list[Force]:
        pass