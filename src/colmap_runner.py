import subprocess
import os


class ColmapRunner:
    def __init__(self):
        # Указываем путь к BAT-файлу COLMAP
        self.colmap_path = r"C:\Users\Mr_Herceg\Downloads\colmap-x64-windows-cuda\COLMAP.bat"

        # Окружение
        self.env = os.environ.copy()
        self.env["COLMAP_NO_GUI"] = "1"

    def _run(self, cmd_list):
        """
        cmd_list — список аргументов, который мы превращаем в строку,
        потому что .bat нельзя запускать списком.
        """
        cmd = " ".join(cmd_list)
        print("Running:", cmd)

        subprocess.run(cmd, check=True, env=self.env, shell=True)

    # -----------------------------
    # FEATURE EXTRACTION
    # -----------------------------
    def run_feature_extractor(self, database_path, image_path):
        cmd = [
            self.colmap_path,
            "feature_extractor",
            "--database_path", f"\"{database_path}\"",
            "--image_path", f"\"{image_path}\"",
        ]
        self._run(cmd)

    # -----------------------------
    # MATCHING
    # -----------------------------
    def run_matcher(self, database_path):
        cmd = [
            self.colmap_path,
            "exhaustive_matcher",
            "--database_path", f"\"{database_path}\"",
        ]
        self._run(cmd)

    # -----------------------------
    # MAPPING
    # -----------------------------
    def run_mapper(self, database_path, image_path, output_path):
        cmd = [
            self.colmap_path,
            "mapper",
            "--database_path", f"\"{database_path}\"",
            "--image_path", f"\"{image_path}\"",
            "--output_path", f"\"{output_path}\"",
        ]
        self._run(cmd)

    # -----------------------------
    # UNDISTORTION
    # -----------------------------
    def run_image_undistorter(self, image_path, sparse_path, dense_path, max_image_size=2000):
        cmd = [
            self.colmap_path,
            "image_undistorter",
            "--image_path", f"\"{image_path}\"",
            "--input_path", f"\"{sparse_path}\"",
            "--output_path", f"\"{dense_path}\"",
            "--output_type", "COLMAP",
            "--max_image_size", str(max_image_size)
        ]
        self._run(cmd)

    # -----------------------------
    # PATCH MATCH
    # -----------------------------
    def run_patch_match_stereo(self, dense_path):
        cmd = [
            self.colmap_path,
            "patch_match_stereo",
            "--workspace_path", f"\"{dense_path}\"",
            "--PatchMatchStereo.geom_consistency", "true"
        ]
        self._run(cmd)

    # -----------------------------
    # STEREO FUSION
    # -----------------------------
    def run_stereo_fusion(self, dense_path, output_path):
        cmd = [
            self.colmap_path,
            "stereo_fusion",
            "--workspace_path", f"\"{dense_path}\"",
            "--output_path", f"\"{output_path}\""
        ]
        self._run(cmd)

    # -----------------------------
    # POISSON MESHING
    # -----------------------------
    def run_poisson_mesher(self, input_path, output_path):
        cmd = [
            self.colmap_path,
            "poisson_mesher",
            "--input_path", f"\"{input_path}\"",
            "--output_path", f"\"{output_path}\""
        ]
        self._run(cmd)
