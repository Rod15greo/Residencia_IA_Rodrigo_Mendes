import tkinter as tk
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
from pyopengltk import OpenGLFrame

class GLWidget(OpenGLFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.image = Image.open("C:/Users/greee/Downloads/EquiView360-main/EquiView360-main/static/example.jpg")
        self.image_width, self.image_height = self.image.size
        self.yaw = 0
        self.pitch = 0
        self.prev_dx = 0
        self.prev_dy = 0
        self.fov = 90
        self.moving = False

    def initgl(self):
        glEnable(GL_TEXTURE_2D)
        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.image_width, self.image_height, 0, GL_RGB, GL_UNSIGNED_BYTE, self.image.tobytes())
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        self.sphere = gluNewQuadric()
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(90, self.winfo_width() / self.winfo_height(), 0.1, 1000)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def redraw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glRotatef(self.pitch, 1, 0, 0)
        glRotatef(self.yaw, 0, 1, 0)
        glRotatef(90, 1, 0, 0)
        glRotatef(-90, 0, 0, 1)
        gluQuadricTexture(self.sphere, True)
        gluSphere(self.sphere, 1, 100, 100)
        glPopMatrix()
        self.tk.call(self._w, 'swapbuffers')

    def on_mouse_press(self, event):
        self.mouse_x, self.mouse_y = event.x, event.y
        self.moving = True

    def on_mouse_release(self, event):
        self.moving = False

    def on_mouse_move(self, event):
        if self.moving:
            dx = event.x - self.mouse_x
            dy = event.y - self.mouse_y
            dx *= 0.1
            dy *= 0.1
            self.yaw -= dx
            self.pitch -= dy
            self.pitch = min(max(self.pitch, -90), 90)
            self.mouse_x, self.mouse_y = event.x, event.y
            self.redraw()

    def on_mouse_wheel(self, event):
        delta = event.delta
        self.fov -= delta * 0.1
        self.fov = max(30, min(self.fov, 90))
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.fov, self.winfo_width() / self.winfo_height(), 0.1, 1000)
        self.redraw()

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Equirectangular 360° Viewer")
        self.geometry("1080x720")
        self.gl_widget = GLWidget(self)
        self.gl_widget.pack(fill=tk.BOTH, expand=True)
        self.gl_widget.bind("<ButtonPress-1>", self.gl_widget.on_mouse_press)
        self.gl_widget.bind("<ButtonRelease-1>", self.gl_widget.on_mouse_release)
        self.gl_widget.bind("<B1-Motion>", self.gl_widget.on_mouse_move)
        self.gl_widget.bind("<MouseWheel>", self.gl_widget.on_mouse_wheel)

if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()
