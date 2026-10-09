from simulation.magnetism.Magnet import Magnet
from simulation.tools.mesh_storage import save_mesh, test
from simulation.tools.force_tables.main import main2
from simulation.types import CarthesianCoordinates

from pathlib import Path

import numpy as np


def export_positions_to_csv(npz_path, csv_path=None):
    npz_path = Path(npz_path)

    # Por padrão, usa o mesmo nome, trocando .npz por .csv.
    csv_path = (
        npz_path.with_suffix(".csv")
        if csv_path is None
        else Path(csv_path)
    )

    with np.load(npz_path, allow_pickle=False) as data:
        positions = data["positions"]

    if positions.ndim != 2 or positions.shape[1] != 3:
        raise ValueError("positions must have shape (n, 3)")

    csv_path.parent.mkdir(parents=True, exist_ok=True)

    np.savetxt(
        csv_path,
        positions,
        delimiter=",",
        header="x,y,z",
        comments="",
        fmt="%.17g",
    )

    return csv_path

# main2()

# CHECK:
#  - Maybe the force-list is unnecessary
#  - Check the interpolation method for multiple magnets and how interfer in HorizontalSurfaceMagnet's
#    update_forces method

#FIXME it's rounding value to zero

path = export_positions_to_csv("./src/data/meshes/test_cylindrical_method.npz")
print(f"CSV saved to: {path}")

test()

# test_magnet = Magnet(
#     radius=10.0,
#     thickness=5.0,
#     magnetization=np.zeros(3),
#     position=CarthesianCoordinates(x=0, y=0, z=0)
# )

# mapping = test_magnet.mapping_pieces_magnet_by_cilindral_method(n_pieces=1000)
# test_magnet.set_magnet_map_in_carthesian_system(mapping=mapping)

# positions = list()
# volumes = list()
# for piece in mapping:
#     positions.append(
#         piece.relative_position.cylindrical_2_carthesian()
#     )

#     volumes.append(
#         piece.volume
#     )

# save_mesh(
#     mesh_id='test_cylindrical_method',
#     positions=positions,
#     radius=test_magnet.radius,
#     thickness=test_magnet.thickness,
#     resolution=20,
#     method='cartesian_grid',
#     volumes=volumes
# )