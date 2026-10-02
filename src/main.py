from simulation.Magnet import Magnet
from simulation.tools.mesh_storage import save_mesh, test
from simulation.tools.force_tables.main import main2

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

main2()

# path = export_positions_to_csv("./src/data/meshes/test.npz")
# print(f"CSV saved to: {path}")

# test()

# test_magnet = Magnet(
#     radius=10.0,
#     thickness=5.0,
#     magnetization=800_000.0
# )

# positions = test_magnet.mapping_pieces_magnet(n_pieces=9000)
# l, w, h = test_magnet.piece_dimensions.values()
# volume_by_piece = l*w*h

# save_mesh(
#     mesh_id='test',
#     positions=positions,
#     radius=test_magnet.radius,
#     thickness=test_magnet.thickness,
#     resolution=20,
#     method='cartesian_grid',
#     volume_by_position=volume_by_piece
# )