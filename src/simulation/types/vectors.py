from numpy import ndarray, dtype, float64, generic

type _Vector3D[ScalarT: generic] = ndarray[tuple[int], dtype[ScalarT]]
type _Array1D[ScalarT: generic] = ndarray[tuple[int], dtype[ScalarT]]
type _Array2D[ScalarT: generic] = ndarray[tuple[int, int], dtype[ScalarT]]

type Vector3D = _Vector3D[float64]
type Array1D = _Array1D[float64]
type Array2D = _Array2D[float64]
