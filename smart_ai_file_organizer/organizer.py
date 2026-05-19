import os
import json
import shutil
import tkinter as tk

from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

from file_reader import get_file_content
from ai_classifier import ask_ai

class SmartFileOrganizer:

    def __init__(self, root):

        self.root = root

        self.root.title("AI智能文件整理器")

        self.root.geometry("1100x700")

        self.folder_path = ""

        self.scan_results = []

        self.move_history = []

        self.create_ui()

    # =====================================

    def create_ui(self):

        top = tk.Frame(self.root)

        top.pack(fill="x", pady=10)

        tk.Button(
            top,
            text="选择目录",
            width=15,
            command=self.select_folder
        ).pack(side="left", padx=5)

        tk.Button(
            top,
            text="扫描文件",
            width=15,
            command=self.scan_files
        ).pack(side="left", padx=5)

        tk.Button(
            top,
            text="开始整理",
            width=15,
            command=self.organize_files
        ).pack(side="left", padx=5)

        tk.Button(
            top,
            text="撤销整理",
            width=15,
            command=self.undo_files
        ).pack(side="left", padx=5)

        self.path_label = tk.Label(
            self.root,
            text="未选择目录",
            fg="blue"
        )

        self.path_label.pack(anchor="w", padx=10)

        columns = (
            "文件名",
            "分类",
            "完整路径"
        )

        self.tree = ttk.Treeview(
            self.root,
            columns=columns,
            show="headings"
        )

        self.tree.heading("文件名", text="文件名")
        self.tree.heading("分类", text="分类")
        self.tree.heading("完整路径", text="完整路径")

        self.tree.column("文件名", width=250)
        self.tree.column("分类", width=150)
        self.tree.column("完整路径", width=650)

        self.tree.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.tree.bind(
            "<Double-1>",
            self.edit_category
        )

    # =====================================

    def select_folder(self):

        folder = filedialog.askdirectory()

        if folder:

            self.folder_path = folder

            self.path_label.config(text=folder)

    # =====================================

    def scan_files(self):

        if not self.folder_path:

            messagebox.showwarning(
                "提示",
                "请先选择目录"
            )

            return

        self.tree.delete(
            *self.tree.get_children()
        )

        self.scan_results.clear()

        for root_dir, dirs, files in os.walk(self.folder_path):

            for file in files:

                path = os.path.join(
                    root_dir,
                    file
                )

                try:

                    content = get_file_content(path)

                    if not content:

                        category = "未分类"

                    else:

                        category = ask_ai(content)

                    item = {
                        "name": file,
                        "path": path,
                        "category": category
                    }

                    self.scan_results.append(item)

                    self.tree.insert(
                        "",
                        "end",
                        values=(
                            file,
                            category,
                            path
                        )
                    )

                    self.root.update()

                except Exception as e:

                    print(e)

        messagebox.showinfo(
            "完成",
            "扫描完成"
        )

    # =====================================

    def edit_category(self, event):

        selected = self.tree.selection()

        if not selected:
            return

        item_id = selected[0]

        values = self.tree.item(
            item_id,
            "values"
        )

        popup = tk.Toplevel(self.root)

        popup.title("修改分类")

        popup.geometry("300x150")

        tk.Label(
            popup,
            text="新的分类:"
        ).pack(pady=10)

        entry = tk.Entry(
            popup,
            width=30
        )

        entry.insert(0, values[1])

        entry.pack(pady=10)

        def save():

            new_category = entry.get()

            self.tree.item(
                item_id,
                values=(
                    values[0],
                    new_category,
                    values[2]
                )
            )

            index = self.tree.index(item_id)

            self.scan_results[index][
                "category"
            ] = new_category

            popup.destroy()

        tk.Button(
            popup,
            text="保存",
            command=save
        ).pack(pady=10)

    # =====================================

    def organize_files(self):

        self.move_history.clear()

        for item in self.scan_results:

            old_path = item["path"]

            category = item["category"]

            filename = os.path.basename(
                old_path
            )

            target_dir = os.path.join(
                self.folder_path,
                category
            )

            os.makedirs(
                target_dir,
                exist_ok=True
            )

            new_path = os.path.join(
                target_dir,
                filename
            )

            try:

                if os.path.abspath(old_path) == os.path.abspath(new_path):
                    continue

                shutil.move(
                    old_path,
                    new_path
                )

                self.move_history.append({
                    "old": old_path,
                    "new": new_path
                })

            except Exception as e:

                print(e)

        history_file = os.path.join(
            self.folder_path,
            "move_history.json"
        )

        with open(
            history_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.move_history,
                f,
                ensure_ascii=False,
                indent=4
            )

        messagebox.showinfo(
            "完成",
            "整理成功"
        )

    # =====================================

    def undo_files(self):

        history_file = os.path.join(
            self.folder_path,
            "move_history.json"
        )

        if not os.path.exists(history_file):

            return

        with open(
            history_file,
            "r",
            encoding="utf-8"
        ) as f:

            history = json.load(f)

        for item in reversed(history):

            try:

                if os.path.exists(item["new"]):

                    os.makedirs(
                        os.path.dirname(item["old"]),
                        exist_ok=True
                    )

                    shutil.move(
                        item["new"],
                        item["old"]
                    )

            except Exception as e:

                print(e)

        messagebox.showinfo(
            "完成",
            "已撤销"
        )