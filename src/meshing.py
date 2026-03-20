from pathlib import Path
from src.colmap_runner import ColmapRunner


def main():
    # Путь к data (на уровень выше src)
    project_dir = Path(__file__).parent.parent / "data"

    dense_dir = project_dir / "dense"
    fused_path = dense_dir / "fused.ply"
    mesh_output = dense_dir / "meshed-poisson.ply"

    # Проверка что есть входной файл
    if not fused_path.exists():
        print(" fused.ply не найден! Сначала запусти dense reconstruction")
        return

    colmap = ColmapRunner()

    print(" Poisson meshing...")
    colmap.run_poisson_mesher(
        str(fused_path.resolve()),
        str(mesh_output.resolve())
    )

    print(f" Mesh готов! -> {mesh_output}")


if __name__ == "__main__":
    main()