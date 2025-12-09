import tkinter as tk
from tkinter import ttk, filedialog, colorchooser, Menu, messagebox
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Data management and Plotter")
        self.root.geometry("800x600")
        
        # Initialize DataFrame with empty strings (default state)
        self.df = pd.DataFrame({
            'X': ['', '', '','', '', '', '', '', '', '', ''],
            'Y1': ['', '', '','', '', '', '', '', '', '', ''], 
            'Y2': ['', '', '','', '', '', '', '', '', '', ''],
            'Y3': ['', '', '','', '', '', '', '', '', '', ''],
            'Y4': ['', '', '','', '', '', '', '', '', '', ''] 
        })
        
        self.setup_ui()
        self.setup_menu()
        self.refresh_table()

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

        # Binding to <Button-1> for single click edit
        self.tree.bind("<Button-1>", self.on_single_click)

    def setup_menu(self):
        menubar = Menu(self.root)
        
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open CSV", command=self.load_csv)
        file_menu.add_command(label="Save CSV", command=self.save_csv)
        file_menu.add_command(label="Random CSV", command=self.random_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        plot_menu = Menu(menubar, tearoff=0)
        plot_menu.add_command(label="Open diagram", command=self.create_plot_window)
        menubar.add_cascade(label="Plot", menu=plot_menu)

        table_menu = Menu(menubar, tearoff=0)
        table_menu.add_command(label="Addition of rows", command=lambda: messagebox.showinfo("Operation", "Addition of rows has not been implemented yet."))
        # Corrected the menu cascade for 'Operations'
        menubar.add_cascade(label="Operations", menu=table_menu) 

        self.root.config(menu=menubar)

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV file", "*.csv")])
        if file_path:
            try:
                self.df = pd.read_csv(file_path)
                self.refresh_table()
            except Exception as e:
                messagebox.showerror("Error", f"Error occured during the reading of the file: {e}")
    
    def random_csv(self, low=0, high=100, row_num=20, col_num=5):
        data = {f'Col_{i}': np.random.randint(low, high, size=row_num) for i in range(col_num)}
        self.df = pd.DataFrame(data)
        self.refresh_table()

    def save_csv(self):
        if self.df is None:
            messagebox.showinfo("Information", "There is not any data for save.")
            return
        
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.df.to_csv(file_path, index=False)
            messagebox.showinfo("Successful", "Files are succesfully saved!")

    def refresh_table(self):
        self.tree.delete(*self.tree.get_children())
        
        if self.df is None:
            return

        cols = list(self.df.columns)
        self.tree["columns"] = cols
        
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")

        # Force UI update to ensure columns are fully configured before inserting rows
        self.tree_frame.update_idletasks() 

        for _, row in self.df.iterrows():
            # Convert values to strings for display to avoid Treeview rendering issues
            display_values = [str(x) for x in list(row)]
            self.tree.insert("", "end", values=display_values)

    def on_single_click(self, event):
        """
        Handles the single click event. Uses root.after to delay the edit initiation,
        ensuring the Treeview selection is processed first.
        """
        region = self.tree.identify_region(event.x, event.y)
        if region != "cell":
            return
        
        # We still need to identify the element IDs now, before the click event finishes
        column_id = self.tree.identify_column(event.x)
        row_id = self.tree.identify_row(event.y)

        if not row_id or self.df is None: 
            return
        
        # Use root.after(1, ...) to schedule the entry widget creation after the event queue
        self.root.after(1, lambda: self._start_cell_edit(column_id, row_id))
        
    def _save_and_update_df(self, entry, row_id, col_index):
        """
        Saves the value from the entry widget to the DataFrame and updates the Treeview.
        This function is called by both FocusOut and movement handlers.
        """
        new_value = entry.get()
        
        try:
            col_name = self.df.columns[col_index]
            typed_value = new_value
            
            # Attempt to convert to float/int if the input looks numeric
            try:
                if "." in new_value:
                    typed_value = float(new_value)
                elif new_value.isdigit() or (new_value.startswith('-') and new_value[1:].isdigit()):
                    typed_value = int(new_value)
                else:
                    typed_value = new_value
            except ValueError:
                typed_value = new_value

            # Update DataFrame and Treeview (important to use new_value for display)
            # FIX: Use col_name (the string identifier) instead of the 1-based index (col_index + 1)
            self.tree.set(row_id, col_name, new_value) 
            self.df.iloc[self.tree.index(row_id), col_index] = typed_value
            
        except Exception:
            pass
            
        finally:
            entry.destroy()

    def _handle_cell_move(self, event, current_entry, current_col_index, current_row_id):
        """
        Saves the current edit and moves the editor to the new cell based on the key press.
        """
        # 1. Save the current content (this also destroys current_entry)
        self._save_and_update_df(current_entry, current_row_id, current_col_index)
        
        # Ensure the operation is finished before calculating the next cell
        self.root.update_idletasks() 

        # 2. Determine target indices
        current_row_index = self.tree.index(current_row_id)
        num_cols = len(self.df.columns)
        num_rows = len(self.df)
        
        target_row_index = current_row_index
        target_col_index = current_col_index
        
        # Calculate new indices based on key
        if event.keysym == "Up":
            target_row_index = max(0, current_row_index - 1)
        elif event.keysym == "Down" or event.keysym == "Return": # Handles Enter key
            target_row_index = min(num_rows - 1, current_row_index + 1)
        elif event.keysym == "Left":
            target_col_index = max(0, current_col_index - 1)
        elif event.keysym == "Right" or event.keysym == "Tab": # NEW: Handle Tab key
            target_col_index = current_col_index + 1
            
            # Check for column wrapping: if we exceed the last column index
            if target_col_index >= num_cols:
                target_col_index = 0      # Wrap to the first column
                target_row_index += 1     # Move to the next row
        else:
            return

        # 3. Get the Treeview IDs for the new cell
        all_row_ids = self.tree.get_children()
        
        if 0 <= target_row_index < num_rows and 0 <= target_col_index < num_cols:
            
            # The column ID format is '#N' where N is 1-based index
            target_column_id = "#" + str(target_col_index + 1)
            target_row_id = all_row_ids[target_row_index]

            # 4. Initiate edit on the new cell (delayed again for reliability)
            self.root.after(1, lambda: self._start_cell_edit(target_column_id, target_row_id))

        
    def _start_cell_edit(self, column_id, row_id):
        """
        Places the Entry widget over the selected cell and sets up bindings.
        """
        
        # Prevent starting a new edit if another Entry is already active
        for widget in self.tree.winfo_children():
            if isinstance(widget, tk.Entry):
                # Ensure the existing entry saves its value before returning
                widget.event_generate('<FocusOut>') 
                return

        try:
            col_index = int(column_id.replace("#", "")) - 1
            row_index = self.tree.index(row_id)
            
            x, y, width, height = self.tree.bbox(row_id, column_id)
            value = self.tree.set(row_id, column_id)

        except ValueError:
            # Catch errors if row/column IDs are invalid
            return
        
        entry = tk.Entry(self.tree, name=f'entry_{row_id}_{column_id}')
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, value)
        entry.focus() # Ensure focus is set
        
        # Bind movement keys (including Enter) to the move handler
        entry.bind("<Key-Up>", lambda e: self._handle_cell_move(e, entry, col_index, row_id))
        entry.bind("<Key-Down>", lambda e: self._handle_cell_move(e, entry, col_index, row_id))
        entry.bind("<Key-Left>", lambda e: self._handle_cell_move(e, entry, col_index, row_id))
        entry.bind("<Key-Right>", lambda e: self._handle_cell_move(e, entry, col_index, row_id))
        
        # NEW: Bind <Key-Tab> to the movement handler
        entry.bind("<Key-Tab>", lambda e: self._handle_cell_move(e, entry, col_index, row_id))
        
        # Bind <Return> to the movement handler
        entry.bind("<Return>", lambda e: self._handle_cell_move(e, entry, col_index, row_id))

        # This simple lambda ensures FocusOut calls the correct save function and destroys the widget.
        entry.bind("<FocusOut>", lambda e: self._save_and_update_df(entry, row_id, col_index))


    def create_plot_window(self):
        
        if self.df is None or self.df.empty or len(self.df.columns) < 2:
            messagebox.showerror("Error", "The CSV file should contain at least two columns (X and Y axes).")
            return

        plot_window = tk.Toplevel(self.root)
        plot_window.title("Interactive Graph")
        plot_window.geometry("800x600")

        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)

        column_names = self.df.columns
        x_col = column_names[0] # The first column is the independent variable (X)

        # Aggressively coerce to numeric and handle NaNs
        try:
            # 1. Convert X data, turning non-numeric strings (like '') into NaN
            x_data_numeric = pd.to_numeric(self.df[x_col], errors='coerce')
            
            # Iterate over all Y columns
            for i in range(1, len(column_names)):
                y_col = column_names[i]
                
                # 2. Convert Y data, turning non-numeric strings (like '') into NaN
                y_data_numeric = pd.to_numeric(self.df[y_col], errors='coerce')
                
                # 3. Combine X and Y data, drop rows where EITHER is NaN (i.e., empty cells)
                plot_data = pd.DataFrame({
                    'X': x_data_numeric,
                    'Y': y_data_numeric
                }).dropna()
                
                # Only plot if we have valid data left
                if not plot_data.empty:
                    ax.plot(
                        plot_data['X'],
                        plot_data['Y'],
                        marker='o',
                        picker=5,
                        label=f"{y_col} vs {x_col}"
                    )
                
        except Exception as e:
            messagebox.showerror("Plotting error", f"Error occured during the conversion/plotting: {e}")
            plot_window.destroy()
            return
        
        ax.legend()
        ax.set_title(f"Data visualization: Y-column as a function of {x_col}")
        ax.set_xlabel(x_col)
        ax.set_ylabel("y-coordinate")
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, plot_window)
        toolbar.update()

        def on_pick(event):
            edit_window = tk.Toplevel(plot_window)
            edit_window.title("Edit Elements")
            edit_window.geometry("250x250")

            def apply_color():
                color = colorchooser.askcolor()[1]
                if color:
                    event.artist.set_color(color)
                    canvas.draw()

            tk.Button(edit_window, text="Color selection", command=apply_color).pack(pady=10)

            def apply_marker(e):
                marker_name = marker_combo.get()
                
                # Map English name back to Matplotlib symbol
                marker_map = {'Circle': 'o', 'Square': 's', 'Triangle': '^', 'Diamond': 'D', 'X': 'x', 'Plus Sign': '+', 'Point': '.'}
                marker = marker_map.get(marker_name, 'o') 
                
                event.artist.set_marker(marker)
                canvas.draw()

            markers = ['o', 's', '^', 'D', 'x', '+', '.']
            marker_names = ['Circle', 'Square', 'Triangle', 'Diamond', 'X', 'Plus Sign', 'Point']
            marker_combo = ttk.Combobox(edit_window, values=marker_names, state="readonly")
            
            # Set initial value based on current marker symbol
            current_marker = event.artist.get_marker()
            if current_marker in markers:
                current_name = marker_names[markers.index(current_marker)]
                marker_combo.set(current_name)
            else:
                marker_combo.set('Circle') # Default if marker is not in the list
                
            marker_combo.bind("<<ComboboxSelected>>", apply_marker)
            marker_combo.pack(pady=10)

            def apply_width(val):
                event.artist.set_linewidth(float(val))
                canvas.draw()

            width_scale = tk.Scale(edit_window, from_=1, to=10, orient="horizontal", command=apply_width, label="Line width")
            width_scale.set(event.artist.get_linewidth())
            width_scale.pack(pady=10, fill="x", padx=10)

        canvas.mpl_connect('pick_event', on_pick)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()