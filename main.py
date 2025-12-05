import tkinter as tk
from tkinter import ttk, filedialog, colorchooser, Menu
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Adatkezelő és Plotter")
        self.root.geometry("800x600")
        self.df = None
        
        self.setup_ui()
        self.setup_menu()

    def setup_ui(self):
        self.tree_frame = ttk.Frame(self.root)
        self.tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(self.tree_frame, show="headings")
        self.v_scroll = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.h_scroll = ttk.Scrollbar(self.tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)

        self.v_scroll.pack(side="right", fill="y")
        self.h_scroll.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True)

        self.tree.bind("<Double-1>", self.on_double_click)

    def setup_menu(self):
        menubar = Menu(self.root)
        
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="CSV Megnyitása", command=self.load_csv)
        file_menu.add_command(label="CSV Mentése", command=self.save_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Kilépés", command=self.root.quit)
        menubar.add_cascade(label="Fájl", menu=file_menu)

        plot_menu = Menu(menubar, tearoff=0)
        plot_menu.add_command(label="Diagram megjelenítése", command=self.create_plot_window)
        menubar.add_cascade(label="Plot", menu=plot_menu)

        self.root.config(menu=menubar)

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV fájlok", "*.csv")])
        if file_path:
            self.df = pd.read_csv(file_path)
            self.refresh_table()

    def save_csv(self):
        if self.df is None:
            return
        
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV fájlok", "*.csv")])
        if file_path:
            self.df.to_csv(file_path, index=False)

    def refresh_table(self):
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = list(self.df.columns)
        
        for col in self.df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")

        for _, row in self.df.iterrows():
            self.tree.insert("", "end", values=list(row))

    def on_double_click(self, event):
        region = self.tree.identify_region(event.x, event.y)
        if region != "cell":
            return
            
        column_id = self.tree.identify_column(event.x)
        row_id = self.tree.identify_row(event.y)
        
        if not row_id: 
            return

        col_index = int(column_id.replace("#", "")) - 1
        row_index = self.tree.index(row_id)
        
        x, y, width, height = self.tree.bbox(row_id, column_id)
        value = self.tree.set(row_id, column_id)

        entry = tk.Entry(self.tree)
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, value)
        entry.focus()

        def save_edit(event=None):
            new_value = entry.get()
            
            try:
                col_name = self.df.columns[col_index]
                if pd.api.types.is_numeric_dtype(self.df[col_name]):
                    if "." in new_value:
                        typed_value = float(new_value)
                    else:
                        typed_value = int(new_value)
                else:
                    typed_value = new_value
            except ValueError:
                typed_value = new_value 

            self.tree.set(row_id, column_id, new_value)
            self.df.iloc[row_index, col_index] = typed_value
            
            entry.destroy()

        entry.bind("<Return>", save_edit)
        entry.bind("<FocusOut>", save_edit)

    def create_plot_window(self):
        if self.df is None or self.df.empty:
            return

        plot_window = tk.Toplevel(self.root)
        plot_window.title("Interaktív Diagram")
        plot_window.geometry("800x600")

        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)

        for data in self.df.columns:
            ax.plot(self.df[data], marker='o', picker=5, label=data)
        
        ax.legend()
        ax.set_title("Test Plot")
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, plot_window)
        toolbar.update()

        def on_pick(event):
            edit_window = tk.Toplevel(plot_window)
            edit_window.title("Elem Szerkesztése")
            edit_window.geometry("250x250")

            def apply_color():
                color = colorchooser.askcolor()[1]
                if color:
                    event.artist.set_color(color)
                    ax.legend()
                    canvas.draw()

            tk.Button(edit_window, text="Színválasztás", command=apply_color).pack(pady=10)

            def apply_marker(e):
                marker = marker_combo.get()
                event.artist.set_marker(marker)
                ax.legend()
                canvas.draw()

            markers = ['o', 's', '^', 'D', 'x', '+', '.']
            marker_combo = ttk.Combobox(edit_window, values=markers, state="readonly")
            marker_combo.set(event.artist.get_marker())
            marker_combo.bind("<<ComboboxSelected>>", apply_marker)
            marker_combo.pack(pady=10)

            def apply_width(val):
                event.artist.set_linewidth(float(val))
                ax.legend()
                canvas.draw()

            width_scale = tk.Scale(edit_window, from_=1, to=10, orient="horizontal", command=apply_width, label="Vonalvastagság")
            width_scale.set(event.artist.get_linewidth())
            width_scale.pack(pady=10, fill="x", padx=10)

        canvas.mpl_connect('pick_event', on_pick)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()