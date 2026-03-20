import subprocess
import os


class ColmapRunner:
    def __init__(self):
        self.colmap_path = r"D:\Colmap\colmap-x64-windows-cuda\colmap.bat"

        self.env = os.environ.copy()

        self.env["QT_QPA_PLATFORM_PLUGIN_PATH"] = r"D:\Colmap\colmap-x64-windows-cuda\plugins\platforms"
        self.env["QT_QPA_PLATFORM"] = "windows"
        self.env["COLMAP_NO_GUI"] = "1"

    def _run(self, cmd):
        print("Running:", " ".join(cmd))
        subprocess.run(cmd, check=True, env=self.env, shell=True)

    def run_feature_extractor(self, database_path, image_path):
        cmd = [
            self.colmap_path,
            "feature_extractor",
            "--database_path", str(database_path),
            "--image_path", str(image_path),
        ]
        self._run(cmd)

    def run_matcher(self, database_path):
        cmd = [
            self.colmap_path,
            "exhaustive_matcher",
            "--database_path", str(database_path),
        ]
        self._run(cmd)

    def run_mapper(self, database_path, image_path, output_path):
        cmd = [
            self.colmap_path,
            "mapper",
            "--database_path", str(database_path),
            "--image_path", str(image_path),
            "--output_path", str(output_path),
        ]
        self._run(cmd)

    def run_image_undistorter(self, image_path, sparse_path, dense_path, max_image_size=2000):
        cmd = [
            self.colmap_path,
            "image_undistorter",
            "--image_path", str(image_path),
            "--input_path", str(sparse_path),
            "--output_path", str(dense_path),
            "--output_type", "COLMAP",
            "--max_image_size", str(max_image_size)
        ]
        self._run(cmd)

    def run_patch_match_stereo(self, dense_path):
        cmd = [
            self.colmap_path,
            "patch_match_stereo",
            "--workspace_path", str(dense_path),
            "--PatchMatchStereo.geom_consistency", "true"
        ]
        self._run(cmd)

    def run_stereo_fusion(self, dense_path, output_path):
        cmd = [
            self.colmap_path,
            "stereo_fusion",
            "--workspace_path", str(dense_path),
            "--output_path", str(output_path)
        ]
        self._run(cmd)

    def run_poisson_mesher(self, input_path, output_path):
        cmd = [
            self.colmap_path,
            "poisson_mesher",
            "--input_path", str(input_path),
            "--output_path", str(output_path)
        ]
        self._run(cmd)