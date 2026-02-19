import tkinter as tk
from tkinter import ttk, filedialog, messagebox, Label
import os
from pyraf import iraf
import re
from PIL import Image, ImageTk


class ImageStackingPipeline:
    def __init__(self, root):
        self.root = root
        self.root.title("IMAGE STACKING SOFTWARE")
        self.root.geometry("900x900")
        self.root.configure(bg="#f0f0f0")

        # Fonts
        self.font_label = ('Segoe UI', 11)
        self.font_title = ('Segoe UI', 13, 'bold')
        self.font_button = ('Segoe UI', 11, 'bold')

        self.output_dir = ""

        # Image Added in Header
        image = Image.open("JCBT.jpg")
        image = image.resize((60, 90))
        self.photo = ImageTk.PhotoImage(image)

        label = Label(root, image=self.photo)
        label.pack(side="right", padx=10, pady=10, anchor="nw")

        # Header
        ttk.Label(root, text="IMAGE STACKING SOFTWARE", font=('Segoe UI', 16, 'bold')).pack(pady=15)

        # xyxymatch Frame
        self.xy_frame = ttk.LabelFrame(root, text="XYXY Match", padding=10)
        self.xy_frame.pack(fill="x", padx=10, pady=10)

        self._add_entry_frame(self.xy_frame, "Input Image:", "Browse", self.browse_xy_input)
        self._add_entry_frame(self.xy_frame, "Reference Image", "Browse", self.browse_xy_ref)
        ttk.Button(self.xy_frame, text="Run xyxy match", command=self.run_xyxymatch).pack(pady=10)

        ttk.Separator(root, orient="horizontal").pack(pady=5)

        # Geomap Frame
        self.geomap_frame = ttk.LabelFrame(root, text="Geomap", padding=10)
        self.geomap_frame.pack(fill="x", padx=10, pady=10)

        self._add_entry_frame(self.geomap_frame, "Input File", "Browse", self.browse_geo_input)
        ttk.Button(self.geomap_frame, text="Run Geomap", command=self.run_geomap).pack(pady=10)

        ttk.Separator(root, orient="horizontal").pack(pady=5)

        # Geotran Frame
        self.geotran_frame = ttk.LabelFrame(root, text="Geotran", padding=10)
        self.geotran_frame.pack(fill="x", padx=10, pady=10)

        self._add_entry_frame(self.geotran_frame, "Fits File", "Browse", self.browse_tran_input)
        self._add_entry_frame(self.geotran_frame, "Matched File", "Browse", self.browse_tran_match)
        self._add_entry_frame(self.geotran_frame, "Database File", "Browse", self.browse_tran_db)
        ttk.Button(self.geotran_frame, text="Run Geotran", command=self.run_geotran).pack(pady=10)

        # ImCombine Frame
        self.imcombine_frame = ttk.LabelFrame(root, text="IMCOMBINE", padding=10)
        self.imcombine_frame.pack(fill="x", padx=10, pady=10)

        self._add_entry_frame(self.imcombine_frame, "B Filter", "Browse", self.browse_b_filter_input)
        self._add_entry_frame(self.imcombine_frame, "V Filter", "Browse", self.browse_v_filter_input)
        self._add_entry_frame(self.imcombine_frame, "R Filter", "Browse", self.browse_r_filter_input)
        self._add_entry_frame(self.imcombine_frame, "I Filter", "Browse", self.browse_i_filter_input)
        self._add_entry_frame(self.imcombine_frame, "Ha Filter", "Browse", self.browse_ha_filter_input)
        self._add_entry_frame(self.imcombine_frame, "Hb Filter", "Browse", self.browse_hb_filter_input)
        ttk.Button(self.imcombine_frame, text="Run Imcombine", command=self.run_imcombine).pack(pady=10)

    # Creating Label Entry and Browse Button
    def _add_entry_frame(self, parent, label_text, button_text, command):
        frame = ttk.Frame(parent)
        frame.pack(fill="x", pady=5)
        ttk.Label(frame, text=label_text, font=self.font_label, width=15).pack(side="left", padx=5)
        entry = ttk.Entry(frame, width=45)
        entry.pack(side="left", padx=5)
        ttk.Button(frame, text=button_text, command=lambda e=entry: command(e)).pack(side="left", padx=5)
        setattr(self, label_text.replace(" ", "_").replace(":", "").lower() + "_entry", entry)

    # Utility to find next available filename
    def get_next_filename(self, directory, base_name, extension):
        existing_files = [f for f in os.listdir(directory) if
                          re.match(f"{base_name}_[0-9]{{3}}{re.escape(extension)}$", f)]
        if not existing_files:
            return f"{base_name}_001{extension}"
        numbers = [int(re.search(r"_(\d{3})", f).group(1)) for f in existing_files]
        next_num = max(numbers) + 1
        return f"{base_name}_{next_num:03d}{extension}"

    # Browser Commands:
    def browse_xy_input(self, entry):
        # file=filedialog.askopenfilename(filetypes=[("Coordinate Files", "*.coo.1")])
        # file=fileopenbox(filetypes=[("Coordinate Files", "*.coo.1")])
        file = filedialog.askopenfilename(filetypes=[("Coordinate Files", "*.coo.1")])
        if file:
            self.input_image_entry.delete(0, tk.END)
            self.input_image_entry.insert(0, file)

    def browse_xy_ref(self, entry):
        file = filedialog.askopenfilenames(filetypes=[("Coordinate Files", "*.coo.1")])
        if file:
            self.reference_image_entry.delete(0, tk.END)
            self.reference_image_entry.insert(0, file)

    def browse_geo_input(self, entry):
        file = filedialog.askopenfilenames(filetypes=[("Matched Coordinate Files", "*.coo")])
        if file:
            self.input_file_entry.delete(0, tk.END)
            self.input_file_entry.insert(0, file)

    def browse_tran_input(self, entry):
        file = filedialog.askopenfilenames(filetypes=[("FITS Files", "*_tbf.fits")])
        if file:
            self.fits_file_entry.delete(0, tk.END)
            self.fits_file_entry.insert(0, file)

    def browse_tran_match(self, entry):
        file = filedialog.askopenfilenames(filetypes=[("Matched Coordinate Files", "*.coo")])
        if file:
            self.matched_file_entry.delete(0, tk.END)
            self.matched_file_entry.insert(0, file)

    def browse_tran_db(self, entry):
        file = filedialog.askopenfilenames(filetypes=[("Database Files", "*.dat")])
        if file:
            self.database_file_entry.delete(0, tk.END)
            self.database_file_entry.insert(0, file)

    def browse_b_filter_input(self, entry):
        # file=filedialog.askopenfilename(filetypes=[("Aligned Fits Files","aligned_*.fits"),("TBF Fits Files","*_tbf.fits"),("All Fits Files","*.fits")])
        file = filedialog.askopenfilenames(filetypes=[("All Fits Files", "*.fits")])
        if file:
            self.b_filter_entry.delete(0, tk.END)
            self.b_filter_entry.insert(0, file)
            # self.aligned_files_entry.insert(0," ".join(file))

    def browse_v_filter_input(self, entry):
        # file=filedialog.askopenfilename(filetypes=[("Aligned Fits Files","aligned_*.fits"),("TBF Fits Files","*_tbf.fits"),("All Fits Files","*.fits")])
        file = filedialog.askopenfilenames(filetypes=[("All Fits Files", "*.fits")])
        if file:
            self.v_filter_entry.delete(0, tk.END)
            self.v_filter_entry.insert(0, file)
            # self.aligned_files_entry.insert(0," ".join(file))

    def browse_r_filter_input(self, entry):
        # file=filedialog.askopenfilename(filetypes=[("Aligned Fits Files","aligned_*.fits"),("TBF Fits Files","*_tbf.fits"),("All Fits Files","*.fits")])
        file = filedialog.askopenfilenames(filetypes=[("All Fits Files", "*.fits")])
        if file:
            self.r_filter_entry.delete(0, tk.END)
            self.r_filter_entry.insert(0, file)
            # self.aligned_files_entry.insert(0," ".join(file))

    def browse_i_filter_input(self, entry):
        # file=filedialog.askopenfilename(filetypes=[("Aligned Fits Files","aligned_*.fits"),("TBF Fits Files","*_tbf.fits"),("All Fits Files","*.fits")])
        file = filedialog.askopenfilenames(filetypes=[("All Fits Files", "*.fits")])
        if file:
            self.i_filter_entry.delete(0, tk.END)
            self.i_filter_entry.insert(0, file)
            # self.aligned_files_entry.insert(0," ".join(file))

    def browse_ha_filter_input(self, entry):
        # file=filedialog.askopenfilename(filetypes=[("Aligned Fits Files","aligned_*.fits"),("TBF Fits Files","*_tbf.fits"),("All Fits Files","*.fits")])
        file = filedialog.askopenfilenames(filetypes=[("All Fits Files", "*.fits")])
        if file:
            self.ha_filter_entry.delete(0, tk.END)
            self.ha_filter_entry.insert(0, file)
            # self.aligned_files_entry.insert(0," ".join(file))

    def browse_hb_filter_input(self, entry):
        # file=filedialog.askopenfilename(filetypes=[("Aligned Fits Files","aligned_*.fits"),("TBF Fits Files","*_tbf.fits"),("All Fits Files","*.fits")])
        file = filedialog.askopenfilenames(filetypes=[("All Fits Files", "*.fits")])
        if file:
            self.hb_filter_entry.delete(0, tk.END)
            self.hb_filter_entry.insert(0, file)
            # self.aligned_files_entry.insert(0," ".join(file))

    # IRAF funtions:
    def run_xyxymatch(self):
        inp = self.input_image_entry.get()
        ref = self.reference_image_entry.get()
        if not (inp and ref):
            messagebox.showerror("Error", "Please select both Input and Reference .coo files.")
            return
        self.output_dir = os.path.dirname(inp)
        os.chdir(self.output_dir)
        out = self.get_next_filename(self.output_dir, "match", ".coo")
        iraf.xyxymatch(input=inp, reference=ref, output=out, tolerance=5, match="triangles")
        messagebox.showinfo("Success", f"XYXYMATCH completed.\nOutput: {out}")

    def run_geomap(self):
        # askopenfilenames returns a list-like string or tuple
        inp_raw = self.input_file_entry.get()
        if not inp_raw:
            messagebox.showerror("Error", "Please provide input match file for GEOMAP.")
            return

        # Extract individual paths (handles spaces and braces from tkinter)
        inp_list = self.root.tk.splitlist(inp_raw)

        self.output_dir = os.path.dirname(inp_list[0])
        os.chdir(self.output_dir)

        created_databases = []
        for single_inp in inp_list:
            # Create a unique database name for each input
            db = self.get_next_filename(self.output_dir, "database", ".dat")
            iraf.geomap(input=single_inp, database=db, fitgeometry="general",
                        xmin=1, xmax=2051, ymin=1, ymax=4086, interactive="no")
            created_databases.append(db)

        messagebox.showinfo("Success",
                            f"GEOMAP completed for {len(inp_list)} files.\nDatabases: {', '.join(created_databases)}")

    def run_geotran(self):
        # Assuming multiple FITS files are selected to be transformed
        fits_raw = self.fits_file_entry.get()
        match = self.matched_file_entry.get()
        db = self.database_file_entry.get()

        if not (fits_raw and match and db):
            messagebox.showerror("Error", "Please fill all GEOTRAN entries.")
            return

        fits_list = self.root.tk.splitlist(fits_raw)
        match_list = self.root.tk.splitlist(match)
        db_list = self.root.tk.splitlist(db)

        if not (len(fits_list) == len(match_list) == len(db_list)):
            messagebox.showerror("Error", f"Mismatched file counts!\nFITS: {len(fits_list)}")
            return

        self.output_dir = os.path.dirname(fits_list[0])
        os.chdir(self.output_dir)

        output_files = []
        for single_fits, single_match, single_db in zip(fits_list, match_list, db_list):
            out = self.get_next_filename(self.output_dir, "aligned", ".fits")
            iraf.geotran(input=single_fits, output=out, database=single_db,
                         transform=single_match, geometry="geometric")
            output_files.append(out)

        messagebox.showinfo("Success",f"GEOTRAN completed for {len(fits_list)} files.\nOutputs: {', '.join(output_files)}")

    def run_imcombine(self):
        # List of filter names as they appear in your labels
        # and the suffix for the output filename
        filters = [
            ("b_filter", "Stacked_B"),
            ("v_filter", "Stacked_V"),
            ("r_filter", "Stacked_R"),
            ("i_filter", "Stacked_I"),
            ("ha_filter", "Stacked_Ha"),
            ("hb_filter", "Stacked_Hb")
        ]

        for attr_prefix, out_suffix in filters:
            try:
                # Construct the dynamic attribute name correctly
                entry_attr = f"{attr_prefix}_entry"
                entry_widget = getattr(self, entry_attr)
                inp = entry_widget.get()

                if not inp:
                    continue  # Skip if no files were selected for this specific filter


                inp_list = self.root.tk.splitlist(inp)

                if not inp_list:
                    continue

                self.output_dir = os.path.dirname(inp_list[0])
                os.chdir(self.output_dir)

                inp_str = ",".join(inp_list)
                out = self.get_next_filename(self.output_dir, out_suffix, ".fits")

                iraf.unlearn(iraf.imcombine)
                iraf.imcombine(input=inp_str, output=out, combine="lmedian", reject="ccdclip")
                messagebox.showinfo("Success", f"IMCOMBINE completed for {out_suffix}.\nOutput: {out}")

            except Exception as e:
                messagebox.showerror("Error", f"Error processing {out_suffix}: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageStackingPipeline(root)
    root.mainloop()