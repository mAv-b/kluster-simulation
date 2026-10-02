from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
MESH_DIR = ROOT / 'data' / 'meshes'

def save_mesh(
    mesh_id:str,
    positions:Any,
    volume_by_position:float,
    radius:float,
    thickness:float,
    resolution:float,
    method:str
) -> Path:
    
    positions = np.asarray(positions, dtype=np.float64)
    if positions.ndim != 2 or positions.shape[1] != 3:
        raise ValueError('positions must have nx3 format')

    MESH_DIR.mkdir(parents=True, exist_ok=True)

    filepath = MESH_DIR / f'{mesh_id}.npz'

    with filepath.open('xb') as file:
        np.savez_compressed(
            file,
            positions=positions,
            volume_by_position=volume_by_position,
            radius=radius,
            thickness=thickness,
            resolution=resolution,
            method=method
        )

    return filepath


def load_mesh(mesh_id:str):
    path = MESH_DIR / f'{mesh_id}.npz'

    with np.load(path, allow_pickle=False) as data:
        mesh = {
            'positions': data['positions'],
            'volume_by_position': data['volume_by_position'].item(),
            'radius': data['radius'].item(),
            'thickness': data['thickness'].item(),
            'resolution': data['resolution'].item(),
            'method': data['method'].item(),
        }

        return mesh


def test():
    with np.load(MESH_DIR / 'test.npz', allow_pickle=False) as data:
        for name in data.files:
            print(f"{name}:")
            print(data[name])
            print()