import tkinter as tk
import customtkinter as ctk
import math
import threading
import time
import core_logic as core

class V_HUD(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("V")
        self.geometry("600x600")
        self.configure(fg_color="#000000")
        self.resizable(False, False)
        self.wm_attributes("-topmost", True)
        self.overrideredirect(True)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - 300
        y = (screen_height // 2) - 300
        self.geometry(f"600x600+{x}+{y}")

        self.canvas = tk.Canvas(self, width=600, height=600, bg="black", highlightthickness=0)
        self.canvas.pack()

        self.angle = 0
        self.pulse = 0.0
        self.pulse_dir = 1
        self.status = "INITIALIZING"
        self.status_color = "#00d4ff"
        self.rotation_speed = 2
        self.running = True
        
        self.canvas.bind("<Button-1>", self.start_move)
        self.canvas.bind("<B1-Motion>", self.do_move)
        self.bind("<Escape>", lambda e: self.quit_app())

        self.draw_hud()
        self.animate()
        
        threading.Thread(target=self.run_v, daemon=True).start()

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f"600x600+{x}+{y}")

    def quit_app(self):
        self.running = False
        self.destroy()

    def draw_hud(self):
        if not self.running: return
        try:
            self.canvas.delete("all")
            cx, cy = 300, 300
            
            r1 = 250
            self.canvas.create_oval(cx-r1, cy-r1, cx+r1, cy+r1, outline="#003e4d", width=2)
            for i in range(0, 360, 20):
                a = math.radians(i + self.angle)
                x1 = cx + (r1-10) * math.cos(a)
                y1 = cy + (r1-10) * math.sin(a)
                x2 = cx + (r1+10) * math.cos(a)
                y2 = cy + (r1+10) * math.sin(a)
                self.canvas.create_line(x1, y1, x2, y2, fill=self.status_color, width=3)

            r2 = 200
            self.canvas.create_arc(cx-r2, cy-r2, cx+r2, cy+r2, start=self.angle*0.5, extent=120, outline="#00d4ff", width=5, style="arc")
            self.canvas.create_arc(cx-r2, cy-r2, cx+r2, cy+r2, start=self.angle*0.5 + 180, extent=120, outline="#00d4ff", width=5, style="arc")

            r3 = 150 + (self.pulse * 5)
            self.canvas.create_oval(cx-r3, cy-r3, cx+r3, cy+r3, outline="#005f73", width=1)
            
            r4 = 100
            self.canvas.create_oval(cx-r4, cy-r4, cx+r4, cy+r4, outline=self.status_color, width=2, fill="#00141a")
            
            display_text = core.config.get("assistant_name", "V").upper()
            self.canvas.create_text(cx, cy, text=display_text, fill="#002b36", font=("Orbitron", 20, "bold"))
            glow_color = self.status_color if self.pulse > 0.5 else "#008ba3"
            self.canvas.create_text(cx, cy-2, text=display_text, fill=glow_color, font=("Orbitron", 21, "bold"))

            self.canvas.create_text(cx, cy+140, text=self.status, fill=self.status_color, font=("Orbitron", 12))
        except:
            pass

    def animate(self):
        if not self.running: return
        if self.status == "THINKING":
            self.rotation_speed = 8
        elif self.status == "LISTENING":
            self.rotation_speed = 4
        else:
            self.rotation_speed = 2
            
        self.angle += self.rotation_speed
        if self.angle >= 360: self.angle = 0
        
        self.pulse += 0.05 * self.pulse_dir
        if self.pulse >= 1 or self.pulse <= 0:
            self.pulse_dir *= -1
            
        try:
            self.draw_hud()
            self.after(30, self.animate)
        except:
            pass

    def run_v(self):
        core.speak(f"Hello {core.config['user_name']}...How may i help you")
        self.status = "ONLINE"
        time.sleep(1)
        
        while True:
            self.status = "LISTENING"
            self.status_color = "#00d4ff"
            query = core.take_command()
            
            if query != "None":
                self.status = "THINKING"
                self.status_color = "#00ffaa"
                response = core.process_query(query)
                
                if response == "SHUTDOWN":
                    core.speak(f"Shutting down System. Goodbye {core.config['user_name']}.")
                    self.quit_app()
                    break
                
                if response:
                    core.speak(response)
            
            self.status = "WAITING"
            self.status_color = "#00d4ff"
            time.sleep(0.5)
            if not self.running: break

if __name__ == "__main__":
    app = V_HUD()
    app.mainloop()
