import os , sys
import tkinter as tk
from tkinter import filedialog , messagebox

try:
    from pyPdf import PdfFileWriter, PdfFileReader
except ImportError:
    try:
        from PyPDF2 import PdfFileWriter, PdfFileReader
    except ImportError:
        exit(-1)


class MergePDFGUI(tk.Frame):   
    def __init__(self, root=None):
        tk.Frame.__init__(self, root)
        self.root = root
        try:
            self.root.iconbitmap(default=self.resource_path("mergepdf.ico"))
        except Exception:
            pass
        self.pdf1 = tk.StringVar()
        self.pdf2 = tk.StringVar()
        self.folder_output = tk.StringVar()
        self.final_pdf = tk.StringVar()
        self.set_design_options()
        self.create_widgets()
        self.set_dir_options()
        self.set_file_options()
    def resource_path(self, relative_path):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)
    def set_design_options(self):
        self.root.title("SUJA PDF Merger")
        self.root.minsize(300, 200)
        self.button_options = {
            'fill': tk.constants.BOTH,
            'padx': 5,
            'pady': 5,
        }

    def create_widgets(self):
        tk.Label(
            self, text='SUJA PDF Merger', font=16,
            ).pack()
        tk.Button(
            self, text='Select first PDF',
            command=lambda: self.set_filename(self.pdf1),
            ).pack(**self.button_options)
        tk.Label(
            self, textvariable=self.pdf1, fg="blue", wraplength=300
            ).pack()
        tk.Button(
            self, text='Select second PDF',
            command=lambda: self.set_filename(self.pdf2),
            ).pack(**self.button_options)
        tk.Label(
            self, textvariable=self.pdf2, fg="blue", wraplength=300
            ).pack()
        tk.Button(
            self, text='Select Output PDF Folder',
            command=lambda: self.set_directory(self.folder_output),
            ).pack(**self.button_options)
        tk.Label(
            self, textvariable=self.folder_output, fg="blue", wraplength=300
            ).pack()
        tk.Label(
            self, text="Input name of final PDF",
            ).pack()
        tk.Entry(
            self, textvariable=self.final_pdf, width=45
            ).pack()
        tk.Label(
            self, text=' '
            ).pack()
        tk.Button(
            self, text='Run', command=self.validate_and_run,
            ).pack(**self.button_options)
    def set_dir_options(self):
        self.directory_options = {
            'initialdir': r'{}'.format(os.getcwd()),
            'parent': self.root,
            'mustexist': False,
            'title': 'Choose a directory',
        }
    def set_file_options(self):
        self.file_options = {
            'initialdir': r'{}'.format(os.getcwd()),
            'parent': self.root,
            'filetypes': (("PDF files", "*.pdf"), ("all files", "*.*")),
            'title': 'Choose a .pdf file',
        }
    def set_filename(self, variable):
        selection = filedialog.askopenfilename(**self.file_options)
        variable.set(selection)
    def set_directory(self, variable):
        selection = filedialog.askdirectory(**self.directory_options)
        variable.set(selection)
    def append_pdf(self, strPFD1, strPDF2, strPDFFinal):
        final_PDF = PdfFileWriter()
        input_PDF1 = PdfFileReader(open(strPFD1, "rb"))
        input_PDF2 = PdfFileReader(open(strPDF2, "rb"))
        [final_PDF.addPage(input_PDF1.getPage(page_num)) for page_num in range(input_PDF1.numPages)]
        [final_PDF.addPage(input_PDF2.getPage(page_num)) for page_num in range(input_PDF2.numPages)]
        final_PDF.write(open(strPDFFinal, "wb"))
    def validate_and_run(self):
        pdf1_is_valid = os.path.exists(self.pdf1.get())
        pdf2_is_valid = os.path.exists(self.pdf2.get())
        folder_output_is_valid = os.path.exists(self.folder_output.get())
        output_name_valid = self.final_pdf.get()
        # Show error if validation failed
        if not pdf1_is_valid:
            messagebox.showerror("Error", "First PDF must be selected")
        elif not pdf2_is_valid:
            messagebox.showerror("Error", "Second PDF must be selected")
        elif not folder_output_is_valid:
            messagebox.showerror("Error", "Output Folder must be selected")
        elif not output_name_valid:
            messagebox.showerror("Error", "Please enter a filename for output (excluding path)")
        else:
            # Determine name for output file(s)
            folder = self.folder_output.get()
            filename = self.final_pdf.get()

            if not filename.endswith(".pdf"):
                filename += ".pdf"

            output_filename = os.path.join(folder, filename)

            # Run the folder compare program
            try:
                self.append_pdf(self.pdf1.get(), self.pdf2.get(), output_filename)

            except Exception:
                messagebox.showerror("Error", "An error has occurred, please try again.")
            else:
                messagebox.showinfo("Success!", "PDF have been merged successfully")
if __name__ == '__main__':
    # Start the app in dev mode
    ROOT = tk.Tk()
    MergePDFGUI(ROOT).pack()
    ROOT.geometry("400x400+200+200")
    ROOT.configure(bg='black')
    ROOT.mainloop()
