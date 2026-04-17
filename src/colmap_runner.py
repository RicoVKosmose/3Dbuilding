import subprocess
import os
from pathlib import Path


class ColmapRunner:
    def __init__(self):
        # === КОРЕНЬ ПРОЕКТА ===
        # src/colmap_runner.py → src → 3Dbuilding
        self.root = Path(__file__).resolve().parent.parent

        # === ПУТЬ К COLMAP.bat ===
        self.colmap_path = str(self.root / "colmap-x64-windows-cuda" / "COLMAP.bat")

        # === ПАПКА С DLL (Qt6, CUDA, COLMAP) ===
        self.colmap_dir = str(self.root / "colmap-x64-windows-cuda")

        # === ОКРУЖЕНИЕ ===
        self.env = os.environ.copy()
        self.env["COLMAP_NO_GUI"] = "1"

        # Добавляем путь к DLL
        self.env["PATH"] = self.colmap_dir + ";" + self.env["PATH"]

    # ============================================================
    # ВНУТРЕННИЙ ЗАПУСК КОМАНДЫ
    # ============================================================
    def _run(self, cmd_list):
        """
        cmd_list — список аргументов, превращаем в строку.
        ВСЕГДА запускаем COLMAP из корня проекта (self.root).
        """
        cmd = " ".join(cmd_list)
        print("Running:", cmd)
        print("Working directory:", self.root)

        subprocess.run(
            cmd,
            check=True,
            env=self.env,
            shell=True,
            cwd=self.root  # <<< ВСЕГДА корень проекта
        )

    # ============================================================
    # FEATURE EXTRACTION
    # ============================================================
    def run_feature_extractor(self, database_path, image_path):
        cmd = [
            f"\"{self.colmap_path}\"",
            "feature_extractor",
            "--database_path", f"\"{database_path}\"",
            "--image_path", f"\"{image_path}\"",
        ]
        self._run(cmd)

    # ============================================================
    # MATCHING
    # ============================================================
    def run_matcher(self, database_path):
        cmd = [
            f"\"{self.colmap_path}\"",
            "exhaustive_matcher",
            "--database_path", f"\"{database_path}\"",
        ]
        self._run(cmd)

    # ============================================================
    # MAPPING
    # ============================================================
    def run_mapper(self, database_path, image_path, output_path):
        cmd = [
            f"\"{self.colmap_path}\"",
            "mapper",
            "--database_path", f"\"{database_path}\"",
            "--image_path", f"\"{image_path}\"",
            "--output_path", f"\"{output_path}\"",
        ]
        self._run(cmd)

    # ============================================================
    # UNDISTORTION
    # ============================================================
    def run_image_undistorter(self, image_path, sparse_path, dense_path, max_image_size=2000):
        cmd = [
            f"\"{self.colmap_path}\"",
            "image_undistorter",
            "--image_path", f"\"{image_path}\"",
            "--input_path", f"\"{sparse_path}\"",
            "--output_path", f"\"{dense_path}\"",
            "--output_type", "COLMAP",
            "--max_image_size", str(max_image_size)
        ]
        self._run(cmd)

    # ============================================================
    # PATCH MATCH
    # ============================================================
    def run_patch_match_stereo(self, dense_path):
        cmd = [
            f"\"{self.colmap_path}\"",
            "patch_match_stereo",
            "--workspace_path", f"\"{dense_path}\"",
            "--PatchMatchStereo.geom_consistency", "true"
        ]
        self._run(cmd)

    # ============================================================
    # STEREO FUSION
    # ============================================================
    def run_stereo_fusion(self, dense_path, output_path):
        cmd = [
            f"\"{self.colmap_path}\"",
            "stereo_fusion",
            "--workspace_path", f"\"{dense_path}\"",
            "--output_path", f"\"{output_path}\""
        ]
        self._run(cmd)

    # ============================================================
    # POISSON MESHING
    # ============================================================
    def run_poisson_mesher(self, input_path, output_path):
        cmd = [
            f"\"{self.colmap_path}\"",
            "poisson_mesher",
            "--input_path", f"\"{input_path}\"",
            "--output_path", f"\"{output_path}\""
        ]
        self._run(cmd)
