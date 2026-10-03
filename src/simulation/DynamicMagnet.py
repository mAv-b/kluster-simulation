import numpy as np

from abc import ABC, abstractmethod

from simulation.types import Vector3D, Force
from .InterpolatedMagnet import InterpolatedMagnet
from .tools.Interpolation import Interpolation


class DynamicMagnet(InterpolatedMagnet, ABC):
    velocity:Vector3D
    angular_velocity:float
    plane_angle:float
    forces_list:list[Force]
    net_force:Vector3D
    net_torque:Vector3D
    trajectory: list[Vector3D]

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

        super().__init__(radius, thickness, magnetization, position, interpolation)

        self.mass = mass
        self.moment_of_inertia = moment_of_inertia

        self.velocity = np.zeros(3)
        self.angular_velocity = 0.0
        self.plane_angle = 0.0

        self.forces_list = list()
        self.net_force = np.zeros(3)
        self.net_torque = np.zeros(3)

        self.trajectory = list([self.position])


    @property
    def aceleration(self):
        return self.net_force / self.mass


    @property
    def angular_acceleration(self):
        return self.net_torque / self.moment_of_inertia


    def add_force(self, force:Vector3D, body_point:Vector3D | None = None) -> Vector3D:
        if body_point is not None:
            vector_displacement = body_point - self.position
            self.add_torque(
                np.cross(vector_displacement, force)
            )

        self.net_force += force

        return force


    def register_force(self, name_force: str, force:Vector3D) -> None:
        self.forces_list.append({
            'force_name': name_force,
            'force_vector': force,
        })


    def add_torque(self, torque:Vector3D) -> Vector3D:
        self.net_torque = torque
        return torque


    def reset_forces(self) -> None:
        self.forces_list.clear()
        self.net_torque = np.zeros(3)
        self.net_force = np.zeros(3)


    def is_moving(self) -> bool:
        return np.linalg.norm(self.net_force) != 0


    @abstractmethod
    def update_forces(self, *args, **kwargs) -> list[Force]:
        # UPDATE THE FORCES IN MAGNET, FOR EACH dt MOVED
        raise NotImplementedError
    

    def move_by_dt(self, dt:float):
        self.velocity += self.velocity + self.aceleration * dt
        self.position += self.position + self.velocity * dt

        self.update_forces()
    
