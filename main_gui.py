import sys
import time
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFileDialog,
    QFileSystemModel,
)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Qt, QThread, Signal
from PySide6.QtGui import QPixmap

from src.colmap_runner import ColmapRunner


# ============================================================
# ПОТОК ДЛЯ ОБРАБОТКИ COLMAP
# ============================================================
class ColmapWorker(QThread):
    progress = Signal(int)
    log = Signal(str)
    finished = Signal()

    def __init__(self, images_dir):
        super().__init__()
        self.images_dir = Path(images_dir)
        self.project_dir = self.images_dir.parent

        self.database_path = self.project_dir / "database.db"
        self.sparse_dir = self.project_dir / "sparse"
        self.sparse_dir.mkdir(exist_ok=True)

        self.dense_dir = self.project_dir / "dense"
        self.dense_dir.mkdir(exist_ok=True)

    def run(self):
        colmap = ColmapRunner()

        steps = [
            ("Feature extraction", lambda: colmap.run_feature_extractor(self.database_path, self.images_dir)),
            ("Matching", lambda: colmap.run_matcher(self.database_path)),
            ("Mapping", lambda: colmap.run_mapper(self.database_path, self.images_dir, self.sparse_dir)),

            # === DENSE RECONSTRUCTION ===
            ("Undistortion", lambda: colmap.run_image_undistorter(
                str(self.images_dir),
                str(self.sparse_dir / "0"),
                str(self.dense_dir)
            )),

            ("PatchMatch Stereo", lambda: colmap.run_patch_match_stereo(
                str(self.dense_dir)
            )),

            ("Stereo Fusion", lambda: colmap.run_stereo_fusion(
                str(self.dense_dir),
                str(self.dense_dir / "fused.ply")
            )),

            ("Poisson Meshing", lambda: colmap.run_poisson_mesher(
                str(self.dense_dir / "fused.ply"),
                str(self.dense_dir / "mesh.ply")
            )),
        ]

        total = len(steps)

        for i, (name, func) in enumerate(steps, start=1):
            self.log.emit(f"🔹 {name}...")
            func()
            self.progress.emit(int(i / total * 100))

        self.log.emit("🎉 Полная 3D‑реконструкция завершена!")
        self.log.emit(f"📦 Модель: {self.dense_dir / 'mesh.ply'}")
        self.finished.emit()



# ============================================================
# ОСНОВНОЕ ОКНО
# ============================================================
class MainWindow(QDialog):
    def __init__(self):
        super().__init__()

        # === ЗАГРУЗКА UI ===
        loader = QUiLoader()
        ui_file = QFile("ui/menu.ui")
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        # === МОДЕЛЬ ДЛЯ treeView ===
        self.model = QFileSystemModel()
        self.model.setReadOnly(True)
        self.ui.treeView.setModel(self.model)

        # === СОСТОЯНИЕ ===
        self.selected_folder = None
        self.worker = None

        # === СИГНАЛЫ ===
        self.ui.pushButton_2.clicked.connect(self.select_folder)
        self.ui.treeView.clicked.connect(self.on_tree_item_clicked)
        self.ui.pushButton.clicked.connect(self.start_processing)

    # ---------------------------------------------------------
    # ВЫБОР ПАПКИ
    # ---------------------------------------------------------
    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку с фото")

        if folder:
            self.selected_folder = folder

            self.model.setRootPath(folder)
            self.ui.treeView.setRootIndex(self.model.index(folder))

            self.ui.plainTextEdit.appendPlainText(f"📁 Выбрана папка: {folder}")

    # ---------------------------------------------------------
    # ПРЕДПРОСМОТР ИЗОБРАЖЕНИЯ
    # ---------------------------------------------------------
    def on_tree_item_clicked(self, index):
        file_path = self.model.filePath(index)

        suffixes = (".jpg", ".jpeg", ".png", ".bmp", ".gif")
        if file_path.lower().endswith(suffixes):
            pixmap = QPixmap(file_path)

            if not pixmap.isNull():
                pixmap = pixmap.scaled(
                    self.ui.previewLabel.width(),
                    self.ui.previewLabel.height(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.ui.previewLabel.setPixmap(pixmap)
                self.ui.plainTextEdit.appendPlainText(f"🖼 Просмотр: {file_path}")
            else:
                self.ui.previewLabel.clear()
        else:
            self.ui.previewLabel.clear()

    # ---------------------------------------------------------
    # ЗАПУСК ОБРАБОТКИ
    # ---------------------------------------------------------
    def start_processing(self):
        if not self.selected_folder:
            self.ui.plainTextEdit.appendPlainText("❌ Сначала выберите папку!")
            return

        self.ui.plainTextEdit.appendPlainText("🚀 Запуск обработки...")

        self.worker = ColmapWorker(self.selected_folder)

        # Сигналы
        self.worker.progress.connect(self.ui.progressBar.setValue)
        self.worker.log.connect(self.ui.plainTextEdit.appendPlainText)
        self.worker.finished.connect(lambda: self.ui.plainTextEdit.appendPlainText("🎉 Все этапы завершены!"))

        self.worker.start()


# ============================================================
# ЗАПУСК ПРИЛОЖЕНИЯ
# ============================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.ui.show()
    sys.exit(app.exec())
