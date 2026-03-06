from pathlib import Path
from src.colmap_runner import ColmapRunner

def main():
    # Уровень проекта
    project_dir = Path(__file__).parent.parent / "data"
    images_dir = project_dir / "images"
    sparse_dir = project_dir / "sparse/0"
    dense_dir = project_dir / "dense"
    dense_dir.mkdir(parents=True, exist_ok=True)

    fused_output = dense_dir / "fused.ply"

    colmap = ColmapRunner()

    print("🔹 Image undistortion...")
    colmap.run_image_undistorter(
        str(images_dir.resolve()),
        str(sparse_dir.resolve()),
        str(dense_dir.resolve())
    )

    print("🔹 Dense stereo reconstruction...")
    colmap.run_patch_match_stereo(str(dense_dir.resolve()))

    print("🔹 Stereo fusion...")
    colmap.run_stereo_fusion(str(dense_dir.resolve()), str(fused_output.resolve()))

    print(f"✅ Dense reconstruction done! Saved to {fused_output}")

if __name__ == "__main__":
    main()