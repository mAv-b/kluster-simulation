from .DynamicMagnet import DynamicMagnet
from .types import Vector3D, Force
from .tools.Interpolation import Interpolation

import numpy as np

class HorizontalSurfaceMagnet(DynamicMagnet):
    _u_static_friction: float
    _u_kinetic_friction: float
    _normal_force:Vector3D

    def __init__(
        self,
        radius: float,
        thickness: float,
        magnetization: Vector3D,
        position: Vector3D,
        mass: float,
        moment_of_inertia: float,
        interpolation: Interpolation
    ) -> None:
        
        super().__init__(
            radius,
            thickness,
            magnetization,
            position,
            mass,
            moment_of_inertia,
            interpolation
        )


    @property
    def normal_force(self) -> Vector3D:
        return self._normal_force


    def set_normal_force(self, gravity:Vector3D) -> None:
        self._normal_force = self.mass * gravity


    @property
    def u_static_friction(self) -> float:
        return self._u_static_friction


    @u_static_friction.setter
    def u_static_friction(self, val:float) -> None:
        if val < 0:
            raise ValueError('Static friction must be a non negative value.')

        self._u_static_friction = val


    @property
    def u_kinetic_friction(self) -> float:
        return self._u_kinetic_friction


    @u_kinetic_friction.setter
    def u_kinetic_friction(self, val:float) -> None:
        if val < 0:
            raise ValueError('kinetic friction must be a non negative value.')

        self._u_kinetic_friction = val


    @property
    def friction_force(self) -> Vector3D:
        velocity_norm = np.linalg.norm(self.velocity)
        normal_force_norm = np.linalg.norm(self.normal_force)
        net_force_norm = np.linalg.norm(self.net_force)

        if velocity_norm == 0:
            max_static_friction_norm = normal_force_norm * self._u_static_friction
            if max_static_friction_norm > net_force_norm:
                return (-1) * self.net_force

            return (-1) * normal_force_norm * self.u_kinetic_friction * (self.net_force / net_force_norm)

        return (-1) * normal_force_norm * self.u_kinetic_friction * (self.velocity / velocity_norm)
        

    def update_forces(self, position) -> list[Force]:
        #verify
        pass