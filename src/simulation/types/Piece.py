from typing import cast, TypedDict

from .coordinates import Coordinates3D, CylindricalCoordinates, CarthesianCoordinates

PieceDimensions = TypedDict(
    'PieceDimensions',
    {
        'length': float,
        'width': float,
        'height': float
    }
)

#TODO implement differents pieces formats

class Piece[C: Coordinates3D]:
    _position:C

    def __init__(
        self,
        relative_position: C,
        volume: float,
        dimensions: PieceDimensions | None = None,
    ) -> None:

        self.dimensions = dimensions
        self.relative_position = relative_position
        self.volume = volume


    @property
    def position(self) -> C:
        return self._position


    #Here is implicit that a coordinate is either a carthesian or a cylindrical
    @position.setter
    def position(self, value:Coordinates3D) -> None:
        if type(value) is type(self.relative_position):
            self._position = self.relative_position + value
        else:
            if isinstance(self.relative_position, CarthesianCoordinates):
                value = cast(CylindricalCoordinates, value)
                self._position = self.relative_position + value.cylindrical_2_carthesian()
            else:
                value = cast(CarthesianCoordinates, value)
                self._position = self.relative_position + value.carthesian_2_cylindrical()


    def __str__(self) -> str:
        return f'{self.__class__} - {self.relative_position} - {self.__hash__}'


    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Piece):
            return False

        return (
            self.relative_position,
            self.volume
        ) == (
            value.relative_position,
            value.volume
        )


    def __hash__(self) -> int:
        return hash((
            self.relative_position,
            self.volume
        ))
