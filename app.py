"""
Smart Emergency Resource Allocator
Algorithm: 0/1 Knapsack using Dynamic Programming
GUI: Python Tkinter (standard library only)

Run: python app.py
"""
import tkinter as tk
from tkinter import ttk, messagebox

class KnapsackSolver:
    """Solves the 0/1 Knapsack problem and retains DP states for visualization."""
    @staticmethod
    def solve(items, capacity):
        n = len(items)
        dp = [[0] * (capacity + 1) for _ in range(n + 1)]

        # Build the dynamic programming table.
        for i in range(1, n + 1):
            weight = items[i - 1]["weight"]
            value = items[i - 1]["value"]
            for cap in range(capacity + 1):
                dp[i][cap] = dp[i - 1][cap]
                if weight <= cap:
                    dp[i][cap] = max(
                        dp[i - 1][cap],
                        value + dp[i - 1][cap - weight]
                    )

        # Backtrack to identify the selected resources.
        selected = []
        cap = capacity
        for i in range(n, 0, -1):
            if dp[i][cap] != dp[i - 1][cap]:
                selected.append(i - 1)
                cap -= items[i - 1]["weight"]
        selected.reverse()
        return dp, selected, dp[n][capacity]


class ResourceAllocatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Emergency Resource Allocator | DAA Project")
        self.root.geometry("1120x760")
        self.root.minsize(950, 650)
        self.root.configure(bg="#eef2f7")
        self.items = [
            {"name": "First Aid Kit", "weight": 4, "value": 10},
            {"name": "Water Pack", "weight": 3, "value": 7},
            {"name": "Food Box", "weight": 5, "value": 12},
            {"name": "Rescue Rope", "weight": 2, "value": 6},
            {"name": "Emergency Radio", "weight": 3, "value": 8},
        ]
        self.dp = None
        self.selected = []
        self.total_value = 0
        self.step_index = 0
        self._style()
        self._build_ui()
        self.refresh_items()

    def _style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=29, font=("Arial", 10),
                        background="white", fieldbackground="white")
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"),
                        background="#dbe5f1", foreground="#17324d")
        style.configure("TButton", font=("Arial", 10, "bold"), padding=7)
        style.configure("TLabel", background="#eef2f7", font=("Arial", 10))

    def _build_ui(self):
        header = tk.Frame(self.root, bg="#15324b", height=86)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="SMART EMERGENCY RESOURCE ALLOCATOR",
                 bg="#15324b", fg="white", font=("Arial", 19, "bold")).pack(anchor="w", padx=24, pady=(15, 2))
        tk.Label(header, text="Optimal resource selection using 0/1 Knapsack • Dynamic Programming",
                 bg="#15324b", fg="#c8d8e8", font=("Arial", 10)).pack(anchor="w", padx=25)

        body = tk.Frame(self.root, bg="#eef2f7")
        body.pack(fill="both", expand=True, padx=18, pady=15)

        left = tk.Frame(body, bg="#eef2f7", width=350)
        left.pack(side="left", fill="y", padx=(0, 14))
        left.pack_propagate(False)

        self._section_title(left, "Resource details")
        form = tk.Frame(left, bg="white", padx=14, pady=14, highlightbackground="#d6dee8", highlightthickness=1)
        form.pack(fill="x", pady=(0, 12))
        self.name_var = tk.StringVar()
        self.weight_var = tk.StringVar()
        self.value_var = tk.StringVar()
        for label, var in [("Resource name", self.name_var), ("Weight (capacity units)", self.weight_var),
                           ("Priority value", self.value_var)]:
            tk.Label(form, text=label, bg="white", fg="#34495e", font=("Arial", 9, "bold")).pack(anchor="w")
            ttk.Entry(form, textvariable=var).pack(fill="x", pady=(3, 9))
        ttk.Button(form, text="Add resource", command=self.add_item).pack(fill="x")

        self._section_title(left, "Available resources")
        list_frame = tk.Frame(left, bg="white", padx=8, pady=8, highlightbackground="#d6dee8", highlightthickness=1)
        list_frame.pack(fill="both", expand=True)
        self.item_tree = ttk.Treeview(list_frame, columns=("weight", "value"), show="tree headings", height=10)
        self.item_tree.heading("#0", text="Resource")
        self.item_tree.heading("weight", text="Weight")
        self.item_tree.heading("value", text="Priority")
        self.item_tree.column("#0", width=150)
        self.item_tree.column("weight", width=65, anchor="center")
        self.item_tree.column("value", width=65, anchor="center")
        self.item_tree.pack(fill="both", expand=True)
        ttk.Button(list_frame, text="Remove selected", command=self.remove_item).pack(fill="x", pady=(8, 0))

        right = tk.Frame(body, bg="#eef2f7")
        right.pack(side="left", fill="both", expand=True)
        self._section_title(right, "Optimization settings")
        settings = tk.Frame(right, bg="white", padx=14, pady=12, highlightbackground="#d6dee8", highlightthickness=1)
        settings.pack(fill="x", pady=(0, 12))
        tk.Label(settings, text="Maximum carrying capacity:", bg="white", font=("Arial", 10, "bold")).pack(side="left")
        self.capacity_var = tk.StringVar(value="10")
        ttk.Entry(settings, textvariable=self.capacity_var, width=8).pack(side="left", padx=10)
        ttk.Button(settings, text="Find optimal allocation", command=self.optimize).pack(side="left")

        self.result_frame = tk.Frame(right, bg="white", padx=14, pady=12, highlightbackground="#d6dee8", highlightthickness=1)
        self.result_frame.pack(fill="x", pady=(0, 12))
        self.result_label = tk.Label(self.result_frame, text="Run the algorithm to view the optimal allocation.",
                                     bg="white", fg="#536779", font=("Arial", 10), justify="left", anchor="w")
        self.result_label.pack(fill="x")

        self._section_title(right, "Dynamic programming visualization")
        visual = tk.Frame(right, bg="white", padx=10, pady=10, highlightbackground="#d6dee8", highlightthickness=1)
        visual.pack(fill="both", expand=True)
        self.step_label = tk.Label(visual, text="The DP table will appear here after optimization.",
                                   bg="white", fg="#34495e", anchor="w", font=("Arial", 9))
        self.step_label.pack(fill="x", pady=(0, 7))
        table_wrap = tk.Frame(visual, bg="white")
        table_wrap.pack(fill="both", expand=True)
        self.dp_tree = ttk.Treeview(table_wrap, show="headings", height=9)
        yscroll = ttk.Scrollbar(table_wrap, orient="vertical", command=self.dp_tree.yview)
        xscroll = ttk.Scrollbar(table_wrap, orient="horizontal", command=self.dp_tree.xview)
        self.dp_tree.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)
        self.dp_tree.pack(side="top", fill="both", expand=True)
        yscroll.pack(side="right", fill="y")
        xscroll.pack(side="bottom", fill="x")
        controls = tk.Frame(visual, bg="white")
        controls.pack(fill="x", pady=(9, 0))
        ttk.Button(controls, text="◀ Previous step", command=self.previous_step).pack(side="left")
        ttk.Button(controls, text="Next step ▶", command=self.next_step).pack(side="left", padx=8)
        ttk.Button(controls, text="Show complete table", command=self.show_full_table).pack(side="right")

        footer = tk.Frame(self.root, bg="#15324b", height=28)
        footer.pack(fill="x", side="bottom")
        tk.Label(footer, text="DAA Assignment 2  |  0/1 Knapsack  |  Time: O(nW)  |  Space: O(nW)",
                 bg="#15324b", fg="white", font=("Arial", 9)).pack(pady=5)

    def _section_title(self, parent, title):
        tk.Label(parent, text=title, bg="#eef2f7", fg="#15324b",
                 font=("Arial", 11, "bold")).pack(anchor="w", pady=(0, 7))

    def refresh_items(self):
        for row in self.item_tree.get_children():
            self.item_tree.delete(row)
        for item in self.items:
            self.item_tree.insert("", "end", text=item["name"],
                                  values=(item["weight"], item["value"]))

    def add_item(self):
        name = self.name_var.get().strip()
        try:
            weight, value = int(self.weight_var.get()), int(self.value_var.get())
            if not name or weight <= 0 or value < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid input", "Enter a name, positive integer weight, and non-negative integer priority.")
            return
        self.items.append({"name": name, "weight": weight, "value": value})
        self.name_var.set(""); self.weight_var.set(""); self.value_var.set("")
        self.refresh_items()
        self.clear_result()

    def remove_item(self):
        chosen = self.item_tree.selection()
        if not chosen:
            messagebox.showinfo("Select resource", "Choose a resource to remove.")
            return
        index = self.item_tree.index(chosen[0])
        self.items.pop(index)
        self.refresh_items()
        self.clear_result()

    def clear_result(self):
        self.dp = None
        self.result_label.config(text="Resource list changed. Run optimization again.")
        self.step_label.config(text="The DP table will appear here after optimization.")
        for row in self.dp_tree.get_children(): self.dp_tree.delete(row)
        self.dp_tree["columns"] = ()

    def optimize(self):
        try:
            capacity = int(self.capacity_var.get())
            if capacity < 0 or capacity > 200:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid capacity", "Capacity must be an integer from 0 to 200.")
            return
        if not self.items:
            messagebox.showerror("No resources", "Add at least one resource before optimization.")
            return
        self.dp, self.selected, self.total_value = KnapsackSolver.solve(self.items, capacity)
        total_weight = sum(self.items[i]["weight"] for i in self.selected)
        names = ", ".join(self.items[i]["name"] for i in self.selected) or "No resources selected"
        self.result_label.config(
            text=f"OPTIMAL PRIORITY: {self.total_value}     |     TOTAL WEIGHT: {total_weight}/{capacity}\n"
                 f"SELECTED RESOURCES: {names}\n"
                 f"Complexity: Time O(n × W), Space O(n × W)  (n = resources, W = capacity)",
            fg="#176b50", font=("Arial", 10, "bold"))
        self.step_index = 0
        self.show_step()

    def _configure_dp_columns(self):
        cols = ["Resource"] + [str(i) for i in range(len(self.dp[0]))]
        self.dp_tree["columns"] = cols
        self.dp_tree.column("Resource", width=130, anchor="w")
        self.dp_tree.heading("Resource", text="Resource")
        for c in cols[1:]:
            self.dp_tree.column(c, width=42, anchor="center", stretch=False)
            self.dp_tree.heading(c, text=c)

    def show_step(self):
        if self.dp is None: return
        self._configure_dp_columns()
        for row in self.dp_tree.get_children(): self.dp_tree.delete(row)
        upto = min(self.step_index + 1, len(self.dp))
        labels = ["No resources"] + [x["name"] for x in self.items]
        for i in range(upto):
            self.dp_tree.insert("", "end", values=[labels[i]] + self.dp[i])
        if self.step_index == 0:
            explanation = "Step 0: Base case — with zero resources, the maximum priority is 0 for every capacity."
        else:
            item = self.items[self.step_index - 1]
            explanation = (f"Step {self.step_index}/{len(self.items)}: Considering {item['name']} "
                           f"(weight {item['weight']}, priority {item['value']}). "
                           "Each cell stores the best result with or without this resource.")
        self.step_label.config(text=explanation)

    def next_step(self):
        if self.dp is None: return
        self.step_index = min(self.step_index + 1, len(self.items))
        self.show_step()

    def previous_step(self):
        if self.dp is None: return
        self.step_index = max(0, self.step_index - 1)
        self.show_step()

    def show_full_table(self):
        if self.dp is None: return
        self.step_index = len(self.items)
        self.show_step()


if __name__ == "__main__":
    root = tk.Tk()
    app = ResourceAllocatorApp(root)
    root.mainloop()
