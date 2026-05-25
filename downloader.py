# -*- coding: utf-8 -*-
"""
Smart Trash Downloader
Tải và cài đặt tất cả dependencies cho Smart Trash Classification System
"""

import os
import sys
import subprocess
import threading
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from pathlib import Path
from typing import Optional
import time


class SmartTrashDownloader:
    """Giao diện download và cài đặt Smart Trash"""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Smart Trash Downloader")
        self.root.geometry("700x600")
        self.root.minsize(600, 500)
        self.root.configure(bg="#F3F6FA")

        # State
        self.installing = False
        self.install_path = Path.home() / "SmartTrash"

        # Variables
        self.path_var = tk.StringVar(value=str(self.install_path))
        self.status_var = tk.StringVar(value="Sẵn sàng cài đặt")
        self.progress_var = tk.DoubleVar(value=0)

        self._build_ui()

    def _build_ui(self) -> None:
        """Xây dựng giao diện"""

        # Header
        header = ttk.Frame(self.root)
        header.pack(fill=tk.X, padx=20, pady=(20, 10))

        ttk.Label(
            header,
            text="🚀 Smart Trash Downloader",
            font=("Segoe UI", 20, "bold"),
            foreground="#2563EB",
        ).pack(anchor=tk.W)

        ttk.Label(
            header,
            text="Tải và cài đặt tất cả dependencies",
            font=("Segoe UI", 10),
            foreground="#6B7280",
        ).pack(anchor=tk.W, pady=(4, 0))

        # Path Selection
        path_frame = ttk.LabelFrame(self.root, text="📁 Thư mục cài đặt", padding=12)
        path_frame.pack(fill=tk.X, padx=20, pady=10)
        path_frame.columnconfigure(1, weight=1)

        ttk.Entry(
            path_frame,
            textvariable=self.path_var,
            state="readonly",
        ).grid(row=0, column=1, sticky=tk.EW, padx=(0, 10))

        ttk.Button(
            path_frame,
            text="Chọn thư mục",
            command=self._choose_path,
        ).grid(row=0, column=2)

        # Installation Steps
        steps_frame = ttk.LabelFrame(self.root, text="📋 Các bước cài đặt", padding=12)
        steps_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        steps_text = tk.Text(
            steps_frame,
            height=12,
            width=70,
            bg="#FFFFFF",
            fg="#374151",
            font=("Courier", 9),
            relief=tk.FLAT,
            state=tk.DISABLED,
        )
        steps_text.pack(fill=tk.BOTH, expand=True)
        self.steps_text = steps_text

        # Add scrollbar
        scrollbar = ttk.Scrollbar(steps_frame, orient=tk.VERTICAL, command=steps_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        steps_text.config(yscrollcommand=scrollbar.set)

        # Status
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill=tk.X, padx=20, pady=(0, 10))

        ttk.Label(status_frame, textvariable=self.status_var, font=("Segoe UI", 9)).pack(
            anchor=tk.W
        )

        # Progress Bar
        self.progress_bar = ttk.Progressbar(
            self.root,
            variable=self.progress_var,
            maximum=100,
            mode="determinate",
        )
        self.progress_bar.pack(fill=tk.X, padx=20, pady=(0, 10))

        # Buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        button_frame.columnconfigure(0, weight=1)

        self.start_btn = ttk.Button(
            button_frame,
            text="🚀 Bắt đầu cài đặt",
            command=self._start_installation,
        )
        self.start_btn.pack(side=tk.RIGHT, padx=5)

        ttk.Button(
            button_frame,
            text="❌ Đóng",
            command=self.root.quit,
        ).pack(side=tk.RIGHT, padx=5)

        # Initial log
        self._log("✅ Downloader sẵn sàng", "info")
        self._log(f"📁 Thư mục cài đặt: {self.install_path}", "info")
        self._log("", "")

    def _log(self, message: str, level: str = "info") -> None:
        """Thêm dòng log"""

        self.steps_text.config(state=tk.NORMAL)

        if level == "info":
            prefix = "ℹ️  "
            self.steps_text.insert(tk.END, f"{prefix}{message}\n", "info")
        elif level == "success":
            prefix = "✅ "
            self.steps_text.insert(tk.END, f"{prefix}{message}\n", "success")
        elif level == "error":
            prefix = "❌ "
            self.steps_text.insert(tk.END, f"{prefix}{message}\n", "error")
        elif level == "warning":
            prefix = "⚠️  "
            self.steps_text.insert(tk.END, f"{prefix}{message}\n", "warning")
        else:
            self.steps_text.insert(tk.END, f"{message}\n")

        self.steps_text.config(state=tk.DISABLED)
        self.steps_text.see(tk.END)
        self.root.update()

    def _choose_path(self) -> None:
        """Chọn thư mục cài đặt"""

        path = filedialog.askdirectory(title="Chọn thư mục cài đặt")
        if path:
            self.install_path = Path(path)
            self.path_var.set(str(self.install_path))

    def _start_installation(self) -> None:
        """Bắt đầu quá trình cài đặt"""

        if self.installing:
            return

        self.installing = True
        self.start_btn.config(state=tk.DISABLED)
        self.steps_text.config(state=tk.NORMAL)
        self.steps_text.delete(1.0, tk.END)
        self.steps_text.config(state=tk.DISABLED)
        self.progress_var.set(0)

        thread = threading.Thread(target=self._install_worker, daemon=True)
        thread.start()

    def _install_worker(self) -> None:
        """Worker thread cho cài đặt"""

        try:
            self._log("🔄 Đang bắt đầu cài đặt...", "info")
            self.root.after(0, lambda: self.status_var.set("Tạo cấu trúc thư mục..."))

            # 1. Create directory structure
            self._create_directories()
            self.root.after(0, lambda: self.progress_var.set(20))

            # 2. Create default files
            self._create_default_files()
            self.root.after(0, lambda: self.progress_var.set(40))

            # 3. Install Python packages
            self.root.after(0, lambda: self.status_var.set("Cài đặt Python packages..."))
            self._install_packages()
            self.root.after(0, lambda: self.progress_var.set(90))

            # 4. Create shortcuts
            self._create_shortcuts()
            self.root.after(0, lambda: self.progress_var.set(100))

            self._log("\n", "")
            self._log("✨ Cài đặt hoàn tất thành công!", "success")
            self._log("", "")
            self._log("📝 Bước tiếp theo:", "info")
            self._log("1. Mở Teachable Machine và export model", "info")
            self._log("2. Sao chép keras_model.h5 vào: model/", "info")
            self._log("3. Chạy: python app.py", "info")

            self.root.after(
                0,
                lambda: messagebox.showinfo(
                    "Hoàn tất",
                    "✅ Cài đặt thành công!\n\n"
                    f"📁 Thư mục: {self.install_path}\n\n"
                    "Bước tiếp theo:\n"
                    "1. Thêm keras_model.h5 vào thư mục model/\n"
                    "2. Chạy: python app.py",
                ),
            )

        except Exception as exc:
            self._log(f"Lỗi: {exc}", "error")
            self.root.after(
                0,
                lambda: messagebox.showerror(
                    "Lỗi cài đặt",
                    f"Đã xảy ra lỗi:\n\n{exc}",
                ),
            )

        finally:
            self.installing = False
            self.root.after(0, lambda: self.start_btn.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.status_var.set("Sẵn sàng"))

    def _create_directories(self) -> None:
        """Tạo cấu trúc thư mục"""

        self._log("📁 Tạo thư mục Smart Trash...", "info")
        (self.install_path / "model").mkdir(parents=True, exist_ok=True)
        (self.install_path / "assets").mkdir(parents=True, exist_ok=True)
        (self.install_path / "Arduino").mkdir(parents=True, exist_ok=True)
        self._log("✅ Thư mục đã tạo", "success")

    def _create_default_files(self) -> None:
        """Tạo file mặc định"""

        self._log("📝 Tạo file cấu hình...", "info")

        # Create default labels.txt
        labels_file = self.install_path / "model" / "labels.txt"
        if not labels_file.exists():
            labels_file.write_text(
                "0 Vô cơ\n1 Hữu cơ\n2 Không thuộc về cả hai loại\n",
                encoding="utf-8",
            )
            self._log("✅ Tạo labels.txt", "success")
        else:
            self._log("⏭️  labels.txt đã có", "info")

        # Create README for model
        readme_model = self.install_path / "model" / "README_MODEL.txt"
        if not readme_model.exists():
            readme_model.write_text(
                "# Teachable Machine Model\n\n"
                "Bước 1: Vào https://teachablemachine.withgoogle.com/\n"
                "Bước 2: Chọn 'Image Project'\n"
                "Bước 3: Train model với 3 lớp rác\n"
                "Bước 4: Export dạng Keras\n"
                "Bước 5: Sao chép keras_model.h5 vào thư mục này\n",
                encoding="utf-8",
            )
            self._log("✅ Tạo README_MODEL.txt", "success")

        # Create Arduino README
        arduino_readme = self.install_path / "Arduino" / "README.txt"
        if not arduino_readme.exists():
            arduino_readme.write_text(
                "# Arduino Servo Control Code\n\n"
                "Bước 1: Mở Arduino IDE\n"
                "Bước 2: Tạo file mới servo_code.ino\n"
                "Bước 3: Sao chép code điều khiển servo\n"
                "Bước 4: Upload vào Arduino\n\n"
                "Nhận lệnh qua Serial (9600 baud):\n"
                "- 'H': Hữu cơ (di chuyển servo)\n"
                "- 'V': Vô cơ (di chuyển servo)\n"
                "- 'I': Idle 90°\n",
                encoding="utf-8",
            )
            self._log("✅ Tạo Arduino/README.txt", "success")

    def _install_packages(self) -> None:
        """Cài đặt Python packages"""

        packages = [
            ("opencv-python>=4.9.0", "OpenCV"),
            ("tensorflow>=2.15.0", "TensorFlow"),
            ("pyserial>=3.5", "PySerial"),
            ("Pillow>=10.0.0", "Pillow"),
            ("numpy>=1.24.0", "NumPy"),
            ("h5py>=3.11.0", "H5PY"),
        ]

        total = len(packages)

        for idx, (package, name) in enumerate(packages):
            self._log(f"📦 Cài đặt {name}...", "info")

            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", "--quiet", package],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                self._log(f"✅ {name} đã cài đặt", "success")
            except subprocess.CalledProcessError as exc:
                self._log(f"⚠️  {name} cài đặt có vấn đề: {exc}", "warning")

            progress = 40 + int((idx + 1) / total * 50)
            self.root.after(0, lambda p=progress: self.progress_var.set(p))

    def _create_shortcuts(self) -> None:
        """Tạo shortcuts để chạy app"""

        self._log("🔗 Tạo batch files...", "info")

        # Create run.bat
        run_bat = self.install_path / "run.bat"
        run_bat.write_text(
            "@echo off\nchcp 65001 >nul\ncd /d \"%~dp0\"\npython app.py\npause\n",
            encoding="utf-8",
        )
        self._log("✅ Tạo run.bat", "success")

        # Create requirements.txt
        req_file = self.install_path / "requirements.txt"
        req_file.write_text(
            "opencv-python>=4.9.0\n"
            "tensorflow>=2.15.0\n"
            "pyserial>=3.5\n"
            "Pillow>=10.0.0\n"
            "numpy>=1.24.0\n"
            "h5py>=3.11.0\n"
            "pyinstaller>=6.0.0\n",
            encoding="utf-8",
        )
        self._log("✅ Tạo requirements.txt", "success")


def main() -> None:
    root = tk.Tk()
    app = SmartTrashDownloader(root)
    root.mainloop()


if __name__ == "__main__":
    main()
