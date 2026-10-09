from math import pi

import numpy as np

from ..types import Vector3D, DipoleOrientation, Coordinates3D

class PointDipole:
    VACUUM_PERMEABILITY = 4 * pi * 1e-7
    MU_0_OVER_4PI = VACUUM_PERMEABILITY / (4 * pi)

    def __init__(
        self,
        position:Coordinates3D,
        magnetic_moment:Vector3D,
    ) -> None:

        self.position = position
        self.magnetic_moment = magnetic_moment


    @property
    def moment_magnitude(self) -> float:
        return np.linalg.norm(self.magnetic_moment)


    @property
    def orientation(self) -> DipoleOrientation:
        orientation_vector = self.magnetic_moment / self.moment_magnitude

        try:
            orientation = DipoleOrientation(orientation_vector)
        except:
            raise ValueError(f'invalid orientation vector for PointDipole: {self.__str__}; invalid orientation: {orientation_vector}')

        return orientation

    
    def magnetic_field_at(self, position:Coordinates3D) -> Vector3D:
        vector_displacement = position.to_vector3D() - self.position.to_vector3D()

        distance = np.linalg.norm(vector_displacement)
        if distance == 0:
            raise ValueError('Dipole Points is in same position...')

        versor_displacement = vector_displacement / distance

        magnetic_moment_displacement_direction:float = np.dot(self.magnetic_moment, versor_displacement)

        magnetic_moment_factor = 3 * (magnetic_moment_displacement_direction) * versor_displacement - self.magnetic_moment

        distance_factor = self.MU_0_OVER_4PI * (1 / (distance)**3)

        return distance_factor * magnetic_moment_factor


    def interaction_energy_with(self, dipole:PointDipole) -> float:
        vector_displacement = dipole.position.to_vector3D() - self.position.to_vector3D()

        distance = np.linalg.norm(vector_displacement)
        if distance == 0:
            raise ValueError('Dipole Points is in same position...')

        versor_displacement = vector_displacement / distance

        dot_magnetic_moment = np.dot(
            self.magnetic_moment, dipole.magnetic_moment)
        
        origin_displacement_dot_magnetic_moment = np.dot(
            self.magnetic_moment, versor_displacement)
        
        target_displacement_dot_magnetic_moment = np.dot(
            dipole.magnetic_moment, versor_displacement)

        distance_factor = ( 1/(distance**3) ) * self.MU_0_OVER_4PI

        return (
            distance_factor * ( dot_magnetic_moment - 3 * (origin_displacement_dot_magnetic_moment) * (target_displacement_dot_magnetic_moment) )
        )


    def force_with(self, dipole:PointDipole) -> Vector3D:
        vector_displacement = self.position.to_vector3D() - dipole.position.to_vector3D()
        
        distance = np.linalg.norm(vector_displacement)
        if distance == 0:
            raise ValueError('Dipole points is in same position')

        versor_displacement = vector_displacement / distance

        dot_magnetic_moment = np.dot(
            self.magnetic_moment, dipole.magnetic_moment)

        origin_magnetic_moment_displacement_direction = np.dot(
            self.magnetic_moment, versor_displacement)

        target_magnetic_moment_displacement_direction = np.dot(
            dipole.magnetic_moment, versor_displacement)

        distance_factor = (3/(distance)**4) * self.MU_0_OVER_4PI

        vector_factor = ( (origin_magnetic_moment_displacement_direction * dipole.magnetic_moment) +
                          (target_magnetic_moment_displacement_direction * self.magnetic_moment) +
                          (dot_magnetic_moment * versor_displacement) -
                          5 * (origin_magnetic_moment_displacement_direction) * (target_magnetic_moment_displacement_direction) * versor_displacement
                         )

        return distance_factor * vector_factor


    def force_from(self, dipole:PointDipole) -> Vector3D:
        return (-1) * self.force_with(dipole)


    def torque_in(self, dipole:PointDipole) -> Vector3D:
        dipole_magnetic_field_at_origin = dipole.magnetic_field_at(self.position)

        return np.cross(
            self.magnetic_moment,
            dipole_magnetic_field_at_origin
        )
