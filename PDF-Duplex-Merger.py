import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader, PdfWriter
import os

class PDFMergeGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PDF Duplex Merger")
        self.geometry("600x300")
        self.configure(bg="#f0f4f7")
        self.pdf_files = []

        self.label = tk.Label(self, text="Drag two PDF files here", font=("Arial", 16), bg="#f0f4f7")
        self.label.pack(pady=10)

        self.listbox = tk.Listbox(self, width=80, height=4, font=("Arial", 12))
        self.listbox.pack(pady=10)
        self.listbox.bind("<Double-Button-1>", self.start_merge)

        self.add_button = tk.Button(self, text="Add files", command=self.add_files, font=("Arial", 12))
        self.add_button.pack(pady=5)

        self.clear_button = tk.Button(self, text="Clear list", command=self.clear_list, font=("Arial", 12))
        self.clear_button.pack(pady=5)

        self.hint = tk.Label(self, text="Double-click a file to start merging (this will be the first file).", bg="#f0f4f7")
        self.hint.pack(pady=10)

    def add_files(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")], title="Select PDF files")
        for file in files:
            if file not in self.pdf_files and len(self.pdf_files) < 2:
                self.pdf_files.append(file)
                self.listbox.insert(tk.END, file)
        if len(self.pdf_files) > 2:
            messagebox.showwarning("Warning", "Please add only two files!")
            self.clear_list()

    def clear_list(self):
        self.pdf_files = []
        self.listbox.delete(0, tk.END)

    def on_drop(self, event):
        files = self.split_drop_files(event.data)
        for file in files:
            if file.lower().endswith(".pdf") and file not in self.pdf_files and len(self.pdf_files) < 2:
                self.pdf_files.append(file)
                self.listbox.insert(tk.END, file)
        if len(self.pdf_files) > 2:
            messagebox.showwarning("Warning", "Please add only two files!")
            self.clear_list()

    @staticmethod
    def split_drop_files(data):
        # Windows: {file1} {file2}, Mac: file1 file2
        return [f.strip("{}") for f in data.split()]

    def start_merge(self, event):
        if len(self.pdf_files) != 2:
            messagebox.showerror("Error", "Please add exactly two PDF files!")
            return

        idx = self.listbox.curselection()
        if not idx:
            messagebox.showerror("Error", "Please select a file!")
            return
        idx = idx[0]
        file1 = self.pdf_files[idx]
        file2 = self.pdf_files[1 - idx]

        try:
            reader1 = PdfReader(file1)
            reader2 = PdfReader(file2)
            n1 = len(reader1.pages)
            n2 = len(reader2.pages)

            if not (n2 == n1 or n2 == n1 - 1):
                messagebox.showerror(
                    "Error",
                    f"The second file must have the same number of pages as the first or exactly one less! ({n1} vs. {n2})"
                )
                return

            base1 = os.path.splitext(os.path.basename(file1))[0]
            base2 = os.path.splitext(os.path.basename(file2))[0]
            output_dir = os.path.dirname(file1)
            output_file = os.path.join(output_dir, f"{base1}_{base2}.pdf")

            writer = PdfWriter()
            pages2 = list(reader2.pages)[::-1]

            for i in range(n2):
                writer.add_page(reader1.pages[i])
                writer.add_page(pages2[i])

            if n1 > n2:
                writer.add_page(reader1.pages[-1])  # Append last page without counterpart

            with open(output_file, "wb") as f_out:
                writer.write(f_out)

            messagebox.showinfo("Success", f"Merging successful!\nFile saved at:\n{output_file}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    try:
        import tkinterdnd2 as tkdnd
        class DnDApp(PDFMergeGUI, tkdnd.TkinterDnD.Tk):
            def __init__(self):
                super().__init__()
                # Enable Drag&Drop for listbox
                self.listbox.drop_target_register('DND_Files')
                self.listbox.dnd_bind('<<Drop>>', self.on_drop)
        app = DnDApp()
    except ImportError:
        # Fallback without Drag&Drop if tkinterdnd2 is not installed
        app = PDFMergeGUI()
    app.mainloop()
