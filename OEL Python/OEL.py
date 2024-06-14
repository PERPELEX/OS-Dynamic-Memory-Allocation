import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter.ttk import Combobox

class MemoryBlock:
    def __init__(self, size, is_occupied=False, occupied_size=0):
        self.size = size
        self.is_occupied = is_occupied
        self.occupied_fragments = [occupied_size] if is_occupied else []

    def free_size(self):
        return self.size - sum(self.occupied_fragments)

    def __str__(self):
        return f'{"Occupied" if self.is_occupied else "Free"} block of size {self.size}KB'

class MemoryManager:
    def __init__(self, blocks):
        self.blocks = [MemoryBlock(size, True if i % 2 == 0 else False, size if i % 2 == 0 else 0) for i, size in enumerate(blocks)]
        # make first block free
        self.blocks[0].is_occupied = False
        self.blocks[0].occupied_fragments = []
        

    def best_fit_allocate(self, request_size):
        best_index = -1
        best_fit_size = float('inf')
        for i, block in enumerate(self.blocks):
            if block.free_size() >= request_size and block.free_size() < best_fit_size:
                best_fit_size = block.free_size()
                best_index = i
        if best_index == -1:
            return None, None
        block = self.blocks[best_index]
        block.occupied_fragments.append(request_size)
        block.is_occupied = True
        internal_fragmentation = block.free_size()
        return best_index, internal_fragmentation

    def deallocate(self, block_index, size_to_free):
        if 0 <= block_index < len(self.blocks):
            block = self.blocks[block_index]
            if size_to_free in block.occupied_fragments:
                block.occupied_fragments.remove(size_to_free)
                block.is_occupied = len(block.occupied_fragments) > 0
                return True
        return False

class MemoryAllocationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Best-Fit Memory Allocation")
        initial_blocks = [2, 120, 20, 150, 160, 1, 4, 554, 124]
        self.memory_manager = MemoryManager(initial_blocks)
        
        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(self.canvas_frame, width=800, height=400)
        self.scrollbar = tk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        self.allocate_button = tk.Button(self.root, text="Allocate Memory", command=self.allocate_memory)
        self.allocate_button.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.deallocate_button = tk.Button(self.root, text="Deallocate Memory", command=self.deallocate_memory)
        self.deallocate_button.pack(side=tk.RIGHT, padx=10, pady=10)
        
        self.update_canvas()

    def update_canvas(self):
        self.canvas.delete("all")
        y = 20
        block_height = 40
        canvas_height = max(len(self.memory_manager.blocks) * block_height + 20, 400)
        self.canvas.config(scrollregion=(0, 0, 800, canvas_height))
        
        for i, block in enumerate(self.memory_manager.blocks):
            total_size = block.size
            occupied_size = sum(block.occupied_fragments)
            free_size = block.free_size()
            occupied_ratio = occupied_size / total_size
            free_ratio = free_size / total_size
            
            self.canvas.create_rectangle(50, y, 50 + 500 * occupied_ratio, y + 30, fill="#ff5959", outline="black")
            self.canvas.create_rectangle(50 + 500 * occupied_ratio, y, 550, y + 30, fill="springgreen2", outline="black")
            
            text = f"Block {i}: Used {occupied_size}KB, Free {free_size}KB"
            self.canvas.create_text(300, y + 15, text=text)
            y += block_height

    def allocate_memory(self):
        request_size = simpledialog.askinteger("Input", "Enter memory size to allocate (KB):", minvalue=1)
        if request_size is not None:
            index, internal_frag = self.memory_manager.best_fit_allocate(request_size)
            if index is not None:
                messagebox.showinfo("Allocation Success", f"Allocated {request_size}KB to block {index}, internal fragmentation: {internal_frag}KB")
            else:
                messagebox.showerror("Allocation Failed", f"Failed to allocate {request_size}KB")
            self.update_canvas()

    def deallocate_memory(self):
        index = simpledialog.askinteger("Input", "Enter block index to deallocate:", minvalue=0, maxvalue=len(self.memory_manager.blocks) - 1)
        if index is not None:
            block = self.memory_manager.blocks[index]
            if block.is_occupied and block.occupied_fragments:
                size_to_free = self.select_fragment_size(block.occupied_fragments)
                if size_to_free:
                    if self.memory_manager.deallocate(index, size_to_free):
                        messagebox.showinfo("Deallocation Success", f"Deallocated {size_to_free}KB from block {index}")
                    else:
                        messagebox.showerror("Deallocation Failed", f"Failed to deallocate {size_to_free}KB from block {index}")
                else:
                    messagebox.showerror("Deallocation Failed", f"Block {index} is already free or has no occupied space")
                self.update_canvas()

    def select_fragment_size(self, fragment_sizes):
        dialog = tk.Toplevel(self.root)
        dialog.title("Select Fragment Size")
        
        label = tk.Label(dialog, text="Select fragment size to deallocate:")
        label.pack(pady=10)
        
        size_var = tk.IntVar()
        combobox = Combobox(dialog, textvariable=size_var, values=fragment_sizes)
        combobox.pack(pady=10)
        combobox.current(0)
        
        def on_confirm():
            dialog.destroy()
        
        button = tk.Button(dialog, text="Confirm", command=on_confirm)
        button.pack(pady=10)
        
        dialog.transient(self.root)
        dialog.grab_set()
        self.root.wait_window(dialog)
        
        return size_var.get()

if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryAllocationApp(root)
    root.mainloop()
