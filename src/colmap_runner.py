import subprocess
import os
from pathlib import Path


class ColmapRunner:
    def __init__(self):
        # Путь к COLMAP.bat
        self.colmap_path = r"C:\Users\Mr_Herceg\Downloads\colmap-x64-windows-cuda\COLMAP.bat"

        # Папка, где лежат DLL и сам COLMAP
        self.colmap_dir = r"C:\Users\Mr_Herceg\Downloads\colmap-x64-windows-cuda"

        # Окружение
        self.env = os.environ.copy()
        self.env["COLMAP_NO_GUI"] = "1"

        # Добавляем путь к DLL
        self.env["PATH"] = self.colmap_dir + ";" + self.env["PATH"]

    def _run(self, cmd_list, project_dir):
        """
        cmd_list — список аргументов, превращаем в строку.
        project_dir — рабочая директория проекта (data/).
        """
        cmd = " ".join(cmd_list)
        print("Running:", cmd)
        print("Working directory:", project_dir)

        subprocess.run(
            cmd,
            check=True,
            env=self.env,
            shell=True,
            cwd=project_dir  # <<< ВСЕГДА data/
        )

    # -----------------------------
    # FEATURE EXTRACTION
    # -----------------------------
    def run_feature_extractor(self, database_path, image_path):
        project_dir = str(Path(database_path).parent)
        cmd = [
            f"\"{self.colmap_path}\"",
            "feature_extractor",
            "--database_path", f"\"{database_path}\"",
            "--image_path", f"\"{image_path}\"",
        ]
        self._run(cmd, project_dir)

    # -----------------------------
    # MATCHING
    # -----------------------------
    def run_matcher(self, database_path):
        project_dir = str(Path(database_path).parent)
        cmd = [
            f"\"{self.colmap_path}\"",
            "exhaustive_matcher",
            "--database_path", f"\"{database_path}\"",
        ]
        self._run(cmd, project_dir)

    # -----------------------------
    # MAPPING
    # -----------------------------
    def run_mapper(self, database_path, image_path, output_path):
        project_dir = str(Path(database_path).parent)
        cmd = [
            f"\"{self.colmap_path}\"",
            "mapper",
            "--database_path", f"\"{database_path}\"",
            "--image_path", f"\"{image_path}\"",
            "--output_path", f"\"{output_path}\"",
        ]
        self._run(cmd, project_dir)

    # -----------------------------
    # UNDISTORTION
    # -----------------------------
    def run_image_undistorter(self, image_path, sparse_path, dense_path, max_image_size=2000):
        project_dir = str(Path(dense_path).parent)
        cmd = [
            f"\"{self.colmap_path}\"",
            "image_undistorter",
            "--image_path", f"\"{image_path}\"",
            "--input_path", f"\"{sparse_path}\"",
            "--output_path", f"\"{dense_path}\"",
            "--output_type", "COLMAP",
            "--max_image_size", str(max_image_size)
        ]
        self._run(cmd, project_dir)

    # -----------------------------
    # PATCH MATCH
    # -----------------------------
    def run_patch_match_stereo(self, dense_path):
        project_dir = str(Path(dense_path).parent)
        cmd = [
            f"\"{self.colmap_path}\"",
            "patch_match_stereo",
            "--workspace_path", f"\"{dense_path}\"",
            "--PatchMatchStereo.geom_consistency", "true"
        ]
        self._run(cmd, project_dir)

    # -----------------------------
    # STEREO FUSION
    # -----------------------------
    def run_stereo_fusion(self, dense_path, output_path):
        project_dir = str(Path(dense_path).parent)
        cmd = [
            f"\"{self.colmap_path}\"",
            "stereo_fusion",
            "--workspace_path", f"\"{dense_path}\"",
            "--output_path", f"\"{output_path}\""
        ]
        self._run(cmd, project_dir)

    # -----------------------------
    # POISSON MESHING
    # -----------------------------
    def run_poisson_mesher(self, input_path, output_path):
        project_dir = str(Path(output_path).parent)
        cmd = [
            f"\"{self.colmap_path}\"",
            "poisson_mesher",
            "--input_path", f"\"{input_path}\"",
            "--output_path", f"\"{output_path}\""
        ]
        self._run(cmd, project_dir)
