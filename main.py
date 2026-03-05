from pathlib import Path
from src.colmap_runner import ColmapRunner

def main():
    project_dir = Path("data")
    images_dir = project_dir / "images"
    database_path = project_dir / "database.db"
    sparse_dir = project_dir / "sparse"

    sparse_dir.mkdir(parents=True, exist_ok=True)

    colmap = ColmapRunner()

    print("🔹 Feature extraction...")
    colmap.run_feature_extractor(database_path, images_dir)

    print("🔹 Matching...")
    colmap.run_matcher(database_path)

    print("🔹 Mapping...")
    colmap.run_mapper(database_path, images_dir, sparse_dir)

    print("✅ Done!")


if __name__ == "__main__":
    main()