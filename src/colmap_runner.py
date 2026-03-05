import subprocess
import os


class ColmapRunner:
    def __init__(self):
        self.colmap_path = r"D:\Colmap\colmap-x64-windows-nocuda\colmap.bat"

        self.env = os.environ.copy()

        self.env["QT_QPA_PLATFORM_PLUGIN_PATH"] = r"D:\Colmap\colmap-x64-windows-nocuda\plugins\platforms"
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