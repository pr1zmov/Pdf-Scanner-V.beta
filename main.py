import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import fitz
import os
import cv2
import numpy as np
from PIL import Image, ImageTk
import io
from threading import Thread
import webbrowser
import subprocess
import sys

class PDFDiagramExtractorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Extractor - By pr1zmov")
        self.root.geometry("800x700")
        self.root.configure(bg='#2c3e50')
        
        
        self.pdf_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.dpi_value = tk.StringVar(value="300")
        self.min_width = tk.StringVar(value="200")
        self.min_height = tk.StringVar(value="100")
        self.min_area = tk.StringVar(value="25000")
        
        
        self.min_diagram_width = 200
        self.min_diagram_height = 100
        self.min_diagram_area = 25000
        
        self.create_widgets()
        
    def create_widgets(self):
        
        title_frame = tk.Frame(self.root, bg='#2c3e50')
        title_frame.pack(pady=20)
        
        title_label = tk.Label(
            title_frame,
            text="PDF Extractor",
            font=("Arial", 18, "bold"),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Extract ONLY Pic",
            font=("Arial", 10),
            bg='#2c3e50',
            fg='#bdc3c7'
        )
        subtitle_label.pack(pady=5)
        
        
        main_container = tk.Frame(self.root, bg='#34495e', relief='raised', bd=2)
        main_container.pack(pady=10, padx=20, fill='both', expand=True)
        
        
        file_frame = tk.LabelFrame(
            main_container, 
            text="Select PDF File", 
            font=("Arial", 11, "bold"),
            bg='#34495e',
            fg='#ecf0f1',
            relief='groove'
        )
        file_frame.pack(pady=15, padx=15, fill='x')
        
        pdf_input_frame = tk.Frame(file_frame, bg='#34495e')
        pdf_input_frame.pack(fill='x', pady=10, padx=10)
        
        self.pdf_entry = tk.Entry(
            pdf_input_frame, 
            textvariable=self.pdf_path, 
            font=("Arial", 10),
            width=60,
            bg='#ecf0f1'
        )
        self.pdf_entry.pack(side='left', fill='x', expand=True)
        
        browse_pdf_btn = tk.Button(
            pdf_input_frame, 
            text="Browse PDF", 
            command=self.browse_pdf,
            bg='#3498db', 
            fg='white',
            font=("Arial", 10, "bold"),
            relief='flat',
            padx=15
        )
        browse_pdf_btn.pack(side='right', padx=(10, 0))
        
        
        output_frame = tk.LabelFrame(
            main_container, 
            text="Output Folder (Optional)", 
            font=("Arial", 11, "bold"),
            bg='#34495e',
            fg='#ecf0f1',
            relief='groove'
        )
        output_frame.pack(pady=15, padx=15, fill='x')
        
        output_input_frame = tk.Frame(output_frame, bg='#34495e')
        output_input_frame.pack(fill='x', pady=10, padx=10)
        
        self.output_entry = tk.Entry(
            output_input_frame, 
            textvariable=self.output_path, 
            font=("Arial", 10),
            width=60,
            bg='#ecf0f1'
        )
        self.output_entry.pack(side='left', fill='x', expand=True)
        
        browse_output_btn = tk.Button(
            output_input_frame, 
            text="Browse Folder", 
            command=self.browse_output,
            bg='#9b59b6', 
            fg='white',
            font=("Arial", 10, "bold"),
            relief='flat',
            padx=15
        )
        browse_output_btn.pack(side='right', padx=(10, 0))
        
        
        settings_frame = tk.LabelFrame(
            main_container, 
            text="Extraction Settings", 
            font=("Arial", 11, "bold"),
            bg='#34495e',
            fg='#ecf0f1',
            relief='groove'
        )
        settings_frame.pack(pady=15, padx=15, fill='x')
        
        
        settings_grid = tk.Frame(settings_frame, bg='#34495e')
        settings_grid.pack(pady=10, padx=10, fill='x')
        
        
        tk.Label(settings_grid, text="DPI Quality:", font=("Arial", 10), bg='#34495e', fg='#ecf0f1').grid(row=0, column=0, sticky='w', pady=5)
        dpi_entry = tk.Entry(settings_grid, textvariable=self.dpi_value, width=10, font=("Arial", 10))
        dpi_entry.grid(row=0, column=1, padx=10, pady=5, sticky='w')
        tk.Label(settings_grid, text="(300 = high quality)", font=("Arial", 8), bg='#34495e', fg='#95a5a6').grid(row=0, column=2, sticky='w', padx=5)
        
        
        tk.Label(settings_grid, text="Min Width:", font=("Arial", 10), bg='#34495e', fg='#ecf0f1').grid(row=1, column=0, sticky='w', pady=5)
        width_entry = tk.Entry(settings_grid, textvariable=self.min_width, width=10, font=("Arial", 10))
        width_entry.grid(row=1, column=1, padx=10, pady=5, sticky='w')
        tk.Label(settings_grid, text="pixels (200 = filters small text)", font=("Arial", 8), bg='#34495e', fg='#95a5a6').grid(row=1, column=2, sticky='w', padx=5)
        
        
        tk.Label(settings_grid, text="Min Height:", font=("Arial", 10), bg='#34495e', fg='#ecf0f1').grid(row=2, column=0, sticky='w', pady=5)
        height_entry = tk.Entry(settings_grid, textvariable=self.min_height, width=10, font=("Arial", 10))
        height_entry.grid(row=2, column=1, padx=10, pady=5, sticky='w')
        tk.Label(settings_grid, text="pixels (100 = reasonable height)", font=("Arial", 8), bg='#34495e', fg='#95a5a6').grid(row=2, column=2, sticky='w', padx=5)
        
       
        tk.Label(settings_grid, text="Min Area:", font=("Arial", 10), bg='#34495e', fg='#ecf0f1').grid(row=3, column=0, sticky='w', pady=5)
        area_entry = tk.Entry(settings_grid, textvariable=self.min_area, width=10, font=("Arial", 10))
        area_entry.grid(row=3, column=1, padx=10, pady=5, sticky='w')
        tk.Label(settings_grid, text="pixels² (25000 = excludes tiny graphics)", font=("Arial", 8), bg='#34495e', fg='#95a5a6').grid(row=3, column=2, sticky='w', padx=5)
        
        
        button_frame = tk.Frame(main_container, bg='#34495e')
        button_frame.pack(pady=20)
        
        self.extract_button = tk.Button(
            button_frame,
            text="Extract Diagrams",
            command=self.start_extraction,
            bg='#e74c3c',
            fg='white',
            font=("Arial", 14, "bold"),
            relief='flat',
            padx=30,
            pady=10
        )
        self.extract_button.pack()
        
        
        self.progress_frame = tk.Frame(main_container, bg='#34495e')
        self.progress_frame.pack(pady=10, fill='x', padx=15)
        
        self.progress = ttk.Progressbar(self.progress_frame, mode='indeterminate', length=400)
        self.progress.pack(pady=5)
        
        self.status_label = tk.Label(
            self.progress_frame,
            text="Ready to extract real diagrams from PDF",
            font=("Arial", 10),
            bg='#34495e',
            fg='#1abc9c'
        )
        self.status_label.pack(pady=5)
        
        
        results_frame = tk.LabelFrame(
            main_container, 
            text="Extraction Log", 
            font=("Arial", 11, "bold"),
            bg='#34495e',
            fg='#ecf0f1',
            relief='groove'
        )
        results_frame.pack(pady=15, padx=15, fill='both', expand=True)
        
        
        text_frame = tk.Frame(results_frame, bg='#34495e')
        text_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.results_text = tk.Text(
            text_frame, 
            height=12, 
            font=("Courier", 9),
            bg='#2c3e50',
            fg='#ecf0f1',
            insertbackground='#ecf0f1'
        )
        
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        self.results_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        
        bottom_frame = tk.Frame(self.root, bg='#2c3e50')
        bottom_frame.pack(pady=10, fill='x')
        
        self.open_folder_btn = tk.Button(
            bottom_frame,
            text="Open Output Folder",
            command=self.open_output_folder,
            bg='#27ae60',
            fg='white',
            font=("Arial", 10, "bold"),
            relief='flat',
            state='disabled'
        )
        self.open_folder_btn.pack(side='left', padx=20)
        
        clear_log_btn = tk.Button(
            bottom_frame,
            text="Clear Log",
            command=self.clear_log,
            bg='#95a5a6',
            fg='white',
            font=("Arial", 10, "bold"),
            relief='flat'
        )
        clear_log_btn.pack(side='right', padx=20)
    
    def browse_pdf(self):
        filename = filedialog.askopenfilename(
            title="Select PDF File",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if filename:
            self.pdf_path.set(filename)
    
    def browse_output(self):
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_path.set(folder)
    
    def clear_log(self):
        self.results_text.delete(1.0, tk.END)
    
    def log_message(self, message, color=None):
        self.results_text.insert(tk.END, message + "\n")
        if color:
            start = self.results_text.index(tk.END + "-1c linestart")
            end = self.results_text.index(tk.END + "-1c")
            self.results_text.tag_add(color, start, end)
            self.results_text.tag_config(color, foreground=color)
        
        self.results_text.see(tk.END)
        self.root.update()
    
    def start_extraction(self):
        if not self.pdf_path.get():
            messagebox.showerror("Error", "Please select a PDF file first!")
            return
        
        try:
            
            self.min_diagram_width = int(self.min_width.get())
            self.min_diagram_height = int(self.min_height.get()) 
            self.min_diagram_area = int(self.min_area.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for all settings!")
            return
        
        
        self.extract_button.config(state='disabled')
        self.open_folder_btn.config(state='disabled')
        self.progress.start()
        self.results_text.delete(1.0, tk.END)
        self.status_label.config(text="Extracting diagrams...", fg='#f39c12')
        
       
        thread = Thread(target=self.extract_diagrams)
        thread.daemon = True
        thread.start()
    
    def extract_diagrams(self):
        try:
            pdf_file = self.pdf_path.get()
            output_folder = self.output_path.get() if self.output_path.get() else None
            dpi = int(self.dpi_value.get()) if self.dpi_value.get() else 300
            
            self.log_message("PDF EXTRACTOR - BY PR1ZMOV", "#3498db")
            self.log_message("=" * 60)
            self.log_message(f"File: {pdf_file}")
            self.log_message(f"Settings: {self.min_diagram_width}x{self.min_diagram_height} min, {self.min_diagram_area} area")
            self.log_message(f"DPI: {dpi}")
            
            if output_folder is None:
                pdf_name = os.path.splitext(os.path.basename(pdf_file))[0]
                output_folder = f"{pdf_name}_diagrams_only"
            
            os.makedirs(output_folder, exist_ok=True)
            self.log_message(f"Output: {output_folder}")
            self.log_message("-" * 60)
            
            doc = fitz.open(pdf_file)
            total_diagrams = 0
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                self.log_message(f"\nPage {page_num + 1}:")
                
                
                embedded_count = self.extract_embedded_diagrams(doc, page, page_num, output_folder)
                
                
                visual_count = self.find_large_visual_structures(page, page_num, output_folder, dpi)
                
                page_total = embedded_count + visual_count
                total_diagrams += page_total
                
                if page_total == 0:
                    self.log_message("    No diagrams found on this page", "#e74c3c")
                else:
                    self.log_message(f"    Found {page_total} diagram(s)", "#27ae60")
            
            doc.close()
            
            self.log_message("\n" + "=" * 60)
            if total_diagrams > 0:
                self.log_message(f"SUCCESS! Found {total_diagrams} real diagrams!", "#27ae60")
                self.log_message(f"Saved to: {output_folder}", "#27ae60")
                self.current_output_folder = output_folder
                self.root.after(0, lambda: self.extraction_complete(output_folder, total_diagrams))
            else:
                self.log_message("No diagrams found in this PDF", "#e67e22")
                self.log_message("This PDF might contain only text or very small graphics", "#95a5a6")
                self.root.after(0, lambda: messagebox.showinfo("No Diagrams", "No diagrams found in this PDF.\n\nThis PDF might contain only text content."))
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.log_message(error_msg, "#e74c3c")
            self.root.after(0, lambda: messagebox.showerror("Extraction Error", str(e)))
        
        finally:
            self.root.after(0, self.extraction_finished)
    
    def extract_embedded_diagrams(self, doc, page, page_num, output_folder):
        diagram_count = 0
        image_list = page.get_images(full=True)
        
        if not image_list:
            return 0
        
        self.log_message(f"   Checking {len(image_list)} embedded image(s)...")
        
        for img_index, img in enumerate(image_list):
            try:
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                
                w, h = pix.width, pix.height
                area = w * h
                
                if w < self.min_diagram_width or h < self.min_diagram_height:
                    self.log_message(f"      Image {img_index+1}: too small ({w}x{h})")
                    pix = None
                    continue
                
                if area < self.min_diagram_area:
                    self.log_message(f"      Image {img_index+1}: area too small ({area} pixels)")
                    pix = None
                    continue
                
                aspect_ratio = w / h
                if aspect_ratio > 10 or aspect_ratio < 0.1:
                    self.log_message(f"      Image {img_index+1}: bad aspect ratio ({aspect_ratio:.2f})")
                    pix = None
                    continue
                
                if pix.n - pix.alpha >= 4:
                    pix = fitz.Pixmap(fitz.csRGB, pix)
                
                diagram_count += 1
                filename = f"diagram_page_{page_num+1:03d}_img_{diagram_count:02d}.png"
                image_path = os.path.join(output_folder, filename)
                pix.save(image_path)
                
                self.log_message(f"      DIAGRAM FOUND: {filename} ({w}x{h})", "#27ae60")
                pix = None
                
            except Exception as e:
                self.log_message(f"      Error processing image {img_index+1}: {e}", "#e74c3c")
        
        return diagram_count
    
    def find_large_visual_structures(self, page, page_num, output_folder, dpi=300):
        try:
            zoom = dpi / 72
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            
            img_data = pix.tobytes("ppm")
            pil_image = Image.open(io.BytesIO(img_data))
            cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            
            self.log_message(f"   Analyzing page layout ({cv_image.shape[1]}x{cv_image.shape[0]})...")
            
            diagram_regions = self.detect_diagram_regions(cv_image)
            
            if not diagram_regions:
                return 0
            
            self.log_message(f"   Found {len(diagram_regions)} potential diagram region(s)")
            
            saved_count = 0
            for i, (x, y, w, h) in enumerate(diagram_regions):
                region_img = cv_image[y:y+h, x:x+w]
                
                if not self.is_likely_diagram(region_img):
                    self.log_message(f"      Region {i+1}: failed diagram validation")
                    continue
                
                saved_count += 1
                filename = f"visual_diagram_page_{page_num+1:03d}_region_{saved_count:02d}.png"
                region_path = os.path.join(output_folder, filename)
                cv2.imwrite(region_path, region_img)
                
                self.log_message(f"      DIAGRAM SAVED: {filename} ({w}x{h})", "#27ae60")
            
            return saved_count
            
        except Exception as e:
            self.log_message(f"   Error analyzing page: {e}", "#e74c3c")
            return 0
    
    def detect_diagram_regions(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        height, width = gray.shape
        
        edges = cv2.Canny(gray, 30, 100, apertureSize=3)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50, minLineLength=30, maxLineGap=10)
        
        line_density_map = np.zeros_like(gray)
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(line_density_map, (x1, y1), (x2, y2), 255, 3)
        
        kernel = np.ones((20, 20), np.uint8)
        line_areas = cv2.dilate(line_density_map, kernel, iterations=2)
        
        contours, _ = cv2.findContours(line_areas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        diagram_regions = []
        
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            
            if w < self.min_diagram_width or h < self.min_diagram_height:
                continue
            
            area = w * h
            if area < self.min_diagram_area:
                continue
            
            aspect_ratio = w / h
            if aspect_ratio > 8 or aspect_ratio < 0.125:
                continue
            
            margin = 20
            if x < margin or y < margin or (x + w) > (width - margin) or (y + h) > (height - margin):
                if w < self.min_diagram_width * 2 or h < self.min_diagram_height * 2:
                    continue
            
            padding = 15
            x = max(0, x - padding)
            y = max(0, y - padding)
            w = min(width - x, w + 2*padding)
            h = min(height - y, h + 2*padding)
            
            diagram_regions.append((x, y, w, h))
        
        return self.remove_overlapping_regions(diagram_regions)
    
    def is_likely_diagram(self, region_img):
        gray = cv2.cvtColor(region_img, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape
        
        edges = cv2.Canny(gray, 50, 150)
        edge_pixels = np.count_nonzero(edges)
        edge_density = edge_pixels / (w * h)
        
        if edge_density < 0.01:
            return False
        
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        geometric_shapes = 0
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 100:
                epsilon = 0.02 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                if len(approx) >= 3:
                    geometric_shapes += 1
        
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=30, minLineLength=20, maxLineGap=5)
        line_count = len(lines) if lines is not None else 0
        
        has_enough_geometry = geometric_shapes >= 2 or line_count >= 5
        has_good_edge_density = edge_density > 0.02
        
        return has_enough_geometry and has_good_edge_density
    
    def remove_overlapping_regions(self, regions):
        if not regions:
            return []
        
        regions = sorted(regions, key=lambda r: r[2] * r[3], reverse=True)
        
        filtered = []
        for region in regions:
            x1, y1, w1, h1 = region
            
            overlaps = False
            for accepted in filtered:
                x2, y2, w2, h2 = accepted
                
                overlap_x = max(0, min(x1 + w1, x2 + w2) - max(x1, x2))
                overlap_y = max(0, min(y1 + h1, y2 + h2) - max(y1, y2))
                overlap_area = overlap_x * overlap_y
                
                region_area = w1 * h1
                if overlap_area / region_area > 0.5:
                    overlaps = True
                    break
            
            if not overlaps:
                filtered.append(region)
        
        return filtered
    
    def extraction_complete(self, output_folder, diagram_count):
        self.status_label.config(text=f"Complete! {diagram_count} diagrams extracted", fg='#27ae60')
        self.open_folder_btn.config(state='normal')
        self.current_output_folder = output_folder
        
        result = messagebox.askyesno(
            "Extraction Complete!",
            f"Successfully extracted {diagram_count} diagrams!\n\n📁 Would you like to open the output folder?"
        )
        
        if result:
            self.open_output_folder()
    
    def extraction_finished(self):
        self.extract_button.config(state='normal')
        self.progress.stop()
    
    def open_output_folder(self):
        if hasattr(self, 'current_output_folder') and os.path.exists(self.current_output_folder):
            try:
                if sys.platform == 'win32':
                    os.startfile(self.current_output_folder)
                elif sys.platform == 'darwin':
                    subprocess.run(['open', self.current_output_folder])
                else:
                    subprocess.run(['xdg-open', self.current_output_folder])
            except Exception as e:
                messagebox.showinfo("Folder Path", f"Output folder:\n{self.current_output_folder}")

def main():
    root = tk.Tk()
    app = PDFDiagramExtractorGUI(root)
    
    
    try:
        root.iconbitmap('icon.ico')
    except:
        pass
    
    root.mainloop()

if __name__ == "__main__":
    main()