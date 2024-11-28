import tkinter as tk

class ResourceBar(tk.Canvas):
    def __init__(self, master, width=200, height=20, max_resource=100, static=False, color="green", **kwargs):
        super().__init__(master, width=width, height=height, **kwargs)
        self.width = width
        self.height = height
        self.max_resource = max_resource
        self.current_resource = max_resource
        self.static = static
        self.color = color
        self.health_bar = self.create_rectangle(0, 0, width, height, fill="grey")
        self.health_bar = self.create_rectangle(0, 0, width, height, fill=color)
        self.update_resource_bar()

    def update_resource_bar(self):
        health_ratio = self.current_resource / self.max_resource
        new_width = self.width * health_ratio
        self.coords(self.health_bar, 0, 0, new_width, self.height)

        if (not self.static):
            if health_ratio > 0.5:
                self.itemconfig(self.health_bar, fill="green")
            elif health_ratio > 0.2:
                self.itemconfig(self.health_bar, fill="yellow")
            else:
                self.itemconfig(self.health_bar, fill="red")

    def set_resource(self, new_health):
        self.current_resource = max(0, min(self.max_resource, new_health))
        self.update_resource_bar()