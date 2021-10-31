import tkinter as tk
import math as m
import numpy as np


def rotatePoint(origin, endpoint, angle):
    tempPoint = (endpoint[0] - origin[0], endpoint[1] - origin[1])
    rad = angle * m.pi / 180
    xPrime = m.cos(rad) * tempPoint[0] - m.sin(rad) * tempPoint[1]
    yPrime = m.sin(rad) * tempPoint[0] + m.cos(rad) * tempPoint[1]

    xPrime += origin[0]
    yPrime += origin[1]

    return xPrime, yPrime


def create_circle(x, y, r, canvas):
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvas.create_oval(x0, y0, x1, y1, fill='#000000')


def shiftCore(x, y):
    # for a rhombus ABCD of page 27 lecture 5
    # input: coords of D
    # output: coords of B & C
    brush_x = x
    brush_y = y
    bCoords = [0, 0]
    cCoords = [0, 0]
    return bCoords, cCoords


def checkPossible(x, y):
    # squaredValue = (x**2) + (y**2)
    # print("New values are x_new={0} and y_new={1}".format(x, y))
    squaredValue = ((300-x)**2) + ((400-y)**2)
    # print("Squared value is {0}".format(squaredValue))
    # Where are these values coming from? Why is maxValue calculated like this? 
    # maxValue = (150**2) + (100**2) + (75**2)
    maxValue = (150 + 100 + 75)**2
    if ((squaredValue >= 0) and (squaredValue <= maxValue)):
        return True
    else:
        return False


class arm:
    def __init__(self, x0, y0, x1, y1, color):
        self.origin = (x0, y0)
        self.endPoint = (x1, y1)
        self.rotationCounter = 0
        self.length = m.sqrt((x1 - x0)**2 + (y1 - y0)**2)


        self.line = canvas.create_line(x0, y0, x1, y1, fill=color, width=5)
    
    def printArm(self):
        print("origin: {0}".format(self.origin))
        print("endpoint: {0}".format(self.endPoint))

class Robot:
    def __init__(self, canv):
        # temp values
        self.floor = arm(250, 400, 350, 400, 'black')
        self.arm1 = arm(300, 400, 300, 250, 'black')
        self.arm2 = arm(300, 250, 300, 150, 'red')
        self.arm3 = arm(300, 150, 300, 75, 'blue')
        self.brush = list(self.arm3.endPoint)  # the coordinates requested by user
        self.paint = False
        self.baseReferencePoint = (450, 400)
        self.canvas = canv
        self.pressed = False

    def translate(self, theta1, theta2, theta3):

        # print("theta 1: {0}, theta 2: {1} theta 3: {2}".format(theta1, theta2, theta3))

        self.arm1.endPoint = rotatePoint(self.arm1.origin, self.baseReferencePoint, theta1)
        self.arm2.origin = self.arm1.endPoint

        arm2ReferencePoint = (self.arm1.endPoint[0] + self.arm2.length, self.arm1.endPoint[1])
        self.arm2.endPoint = rotatePoint(self.arm2.origin, arm2ReferencePoint, theta1 + theta2)
        self.arm3.origin = self.arm2.endPoint

        arm3ReferencePoint = (self.arm2.endPoint[0] + self.arm3.length, self.arm2.endPoint[1])
        self.arm3.endPoint = rotatePoint(self.arm3.origin, arm3ReferencePoint, theta1 + theta2 + theta3)

        # self.arm1.printArm()
        # self.arm2.printArm()
        # self.arm3.printArm()

        canvas.coords(self.arm1.line, self.arm1.origin[0], self.arm1.origin[1], self.arm1.endPoint[0],
                      self.arm1.endPoint[1])
        canvas.coords(self.arm2.line, self.arm2.origin[0], self.arm2.origin[1], self.arm2.endPoint[0],
                      self.arm2.endPoint[1])
        canvas.coords(self.arm3.line, self.arm3.origin[0], self.arm3.origin[1], self.arm3.endPoint[0],
                      self.arm3.endPoint[1])

    def arm1CW(self, event=-1):

        self.arm1.endPoint = rotatePoint(self.arm1.origin, self.arm1.endPoint, 1)
        self.arm2.origin = self.arm1.endPoint
        self.arm2.endPoint = rotatePoint(self.arm1.origin, self.arm2.endPoint, 1)
        self.arm3.origin = self.arm2.endPoint
        self.arm3.endPoint = rotatePoint(self.arm1.origin, self.arm3.endPoint, 1)
        self.brush = [self.arm3.endPoint[0], self.arm3.endPoint[1]]

        self.arm1.rotationCounter += 1

        canvas.coords(self.arm1.line, self.arm1.origin[0], self.arm1.origin[1], self.arm1.endPoint[0],
                      self.arm1.endPoint[1])
        canvas.coords(self.arm2.line, self.arm2.origin[0], self.arm2.origin[1], self.arm2.endPoint[0],
                      self.arm2.endPoint[1])
        canvas.coords(self.arm3.line, self.arm3.origin[0], self.arm3.origin[1], self.arm3.endPoint[0],
                      self.arm3.endPoint[1])

        if self.paint:
            circle = create_circle(self.arm3.endPoint[0], self.arm3.endPoint[1], 10, self.canvas)

    def arm1CCW(self, event=-1):

        self.arm1.endPoint = rotatePoint(self.arm1.origin, self.arm1.endPoint, -1)
        self.arm2.origin = self.arm1.endPoint
        self.arm2.endPoint = rotatePoint(self.arm1.origin, self.arm2.endPoint, -1)
        self.arm3.origin = self.arm2.endPoint
        self.arm3.endPoint = rotatePoint(self.arm1.origin, self.arm3.endPoint, -1)
        self.brush = [self.arm3.endPoint[0], self.arm3.endPoint[1]]

        self.arm1.rotationCounter -= 1

        canvas.coords(self.arm1.line, self.arm1.origin[0], self.arm1.origin[1], self.arm1.endPoint[0],
                      self.arm1.endPoint[1])
        canvas.coords(self.arm2.line, self.arm2.origin[0], self.arm2.origin[1], self.arm2.endPoint[0],
                      self.arm2.endPoint[1])
        canvas.coords(self.arm3.line, self.arm3.origin[0], self.arm3.origin[1], self.arm3.endPoint[0],
                      self.arm3.endPoint[1])

        if self.paint:
            circle = create_circle(self.arm3.endPoint[0], self.arm3.endPoint[1], 10, self.canvas)

    def arm2CW(self, event=-1):

        self.arm2.endPoint = rotatePoint(self.arm2.origin, self.arm2.endPoint, 1)
        self.arm3.origin = self.arm2.endPoint
        self.arm3.endPoint = rotatePoint(self.arm2.origin, self.arm3.endPoint, 1)
        self.brush = [self.arm3.endPoint[0], self.arm3.endPoint[1]]

        self.arm2.rotationCounter += 1

        canvas.coords(self.arm1.line, self.arm1.origin[0], self.arm1.origin[1], self.arm1.endPoint[0],
                      self.arm1.endPoint[1])
        canvas.coords(self.arm2.line, self.arm2.origin[0], self.arm2.origin[1], self.arm2.endPoint[0],
                      self.arm2.endPoint[1])
        canvas.coords(self.arm3.line, self.arm3.origin[0], self.arm3.origin[1], self.arm3.endPoint[0],
                      self.arm3.endPoint[1])

        if self.paint:
            circle = create_circle(self.arm3.endPoint[0], self.arm3.endPoint[1], 10, self.canvas)

    def arm2CCW(self, event=-1):

        self.arm2.endPoint = rotatePoint(self.arm2.origin, self.arm2.endPoint, -1)
        self.arm3.origin = self.arm2.endPoint
        self.arm3.endPoint = rotatePoint(self.arm2.origin, self.arm3.endPoint, -1)
        self.brush = [self.arm3.endPoint[0], self.arm3.endPoint[1]]

        self.arm2.rotationCounter -= 1

        canvas.coords(self.arm1.line, self.arm1.origin[0], self.arm1.origin[1], self.arm1.endPoint[0],
                      self.arm1.endPoint[1])
        canvas.coords(self.arm2.line, self.arm2.origin[0], self.arm2.origin[1], self.arm2.endPoint[0],
                      self.arm2.endPoint[1])
        canvas.coords(self.arm3.line, self.arm3.origin[0], self.arm3.origin[1], self.arm3.endPoint[0],
                      self.arm3.endPoint[1])

        if self.paint:
            circle = create_circle(self.arm3.endPoint[0], self.arm3.endPoint[1], 10, self.canvas)

    def arm3CW(self, event=-1):

        self.arm3.endPoint = rotatePoint(self.arm3.origin, self.arm3.endPoint, 1)
        self.brush = [self.arm3.endPoint[0], self.arm3.endPoint[1]]

        self.arm3.rotationCounter += 1

        canvas.coords(self.arm1.line, self.arm1.origin[0], self.arm1.origin[1], self.arm1.endPoint[0],
                      self.arm1.endPoint[1])
        canvas.coords(self.arm2.line, self.arm2.origin[0], self.arm2.origin[1], self.arm2.endPoint[0],
                      self.arm2.endPoint[1])
        canvas.coords(self.arm3.line, self.arm3.origin[0], self.arm3.origin[1], self.arm3.endPoint[0],
                      self.arm3.endPoint[1])

        if self.paint:
            circle = create_circle(self.arm3.endPoint[0], self.arm3.endPoint[1], 10, self.canvas)

    def arm3CCW(self, event=-1):

        self.arm3.endPoint = rotatePoint(self.arm3.origin, self.arm3.endPoint, -1)
        self.brush = [self.arm3.endPoint[0], self.arm3.endPoint[1]]

        self.arm3.rotationCounter -= 1

        canvas.coords(self.arm1.line, self.arm1.origin[0], self.arm1.origin[1], self.arm1.endPoint[0],
                      self.arm1.endPoint[1])
        canvas.coords(self.arm2.line, self.arm2.origin[0], self.arm2.origin[1], self.arm2.endPoint[0],
                      self.arm2.endPoint[1])
        canvas.coords(self.arm3.line, self.arm3.origin[0], self.arm3.origin[1], self.arm3.endPoint[0],
                      self.arm3.endPoint[1])

        if self.paint:
            circle = create_circle(self.arm3.endPoint[0], self.arm3.endPoint[1], 10, self.canvas)

    def togglePaint(self, event=-1):
        print("paintbrush toggled!")
        circle = create_circle(self.arm3.endPoint[0], self.arm3.endPoint[1], 10, self.canvas)
        self.paint = not self.paint

    def left(self, event=-1):
        xleft = self.brush[0] - 7
        yleft = self.brush[1]

        if (checkPossible(xleft, yleft)):
            self.brush[0] -= 7
            theta1, theta2, theta3 = self.brushShift()
            self.translate(theta1, theta2, theta3)
        else:
            print("Hey, thats out of bounds!")

        if self.paint:
            circle = create_circle(self.arm3.endPoint[0], self.arm3.endPoint[1], 10, self.canvas)

    def right(self, event=-1):
        xright = self.brush[0] + 7
        yright = self.brush[1]

        if (checkPossible(xright, yright)):
            self.brush[0] += 7
            theta1, theta2, theta3 = self.brushShift()
            self.translate(theta1, theta2, theta3)

        else:
            print("Hey, thats out of bounds!")

        if self.paint:
            circle = create_circle(self.arm3.endPoint[0], self.arm3.endPoint[1], 10, self.canvas)

    def up(self, event=-1):
        xup = self.brush[0]
        yup = self.brush[1] - 7

        if (checkPossible(xup, yup)):
            self.brush[1] -= 7
            theta1, theta2, theta3 = self.brushShift()
            self.translate(theta1, theta2, theta3)

        else:
            print("Hey, thats out of bounds!")

        if self.paint:
            circle = create_circle(self.arm3.endPoint[0], self.arm3.endPoint[1], 10, self.canvas)

    def down(self, event=-1):
        xdown = self.brush[0]
        ydown = self.brush[1] + 7

        if (checkPossible(xdown, ydown)):
            self.brush[1] += 7
            theta1, theta2, theta3 = self.brushShift()
            self.translate(theta1, theta2, theta3)
        else:
            print("Hey, thats out of bounds!")


        if self.paint:
            circle = create_circle(self.arm3.endPoint[0], self.arm3.endPoint[1], 10, self.canvas)

    #  input: brush x y
    #  output: theta 1, 2, 3 in degree
    def brushShift(self):
        brush_x = self.brush[0]
        brush_y = self.brush[1]

        #
        # alpha = m.atan((400-brush_y)/(brush_x-300))
        #
        # link1_y = 150 * m.sin(alpha)
        # link1_x = 150 * m.cos(alpha)
        #
        # beta2_1 = m.atan(((link1_y - brush_y) / (brush_x - link1_x)))
        #
        # theta1 = 0
        # theta2 = 0
        # theta3 = 0
        #
        # theta1 = theta1 * 180/m.pi
        # theta2 = theta2 * 180/m.pi
        # theta3 = theta3 * 180/m.pi
        # alpha = alpha * 180/m.pi
        # beta2_1 = beta2_1 * 180/m.pi
        #
        #
        # print("Brush coords: {0},{1}".format(self.brush[0], self.brush[1]))
        # print("Alpha: {0}".format(alpha))
        # print("link1 and 2: {0} {1}".format(link1_x, link1_y))
        # print("Beta: {0}".format(beta2_1))
        # print("Thetas: {0}, {1}, {2}".format(theta1, theta2, theta3))


        # ------------------------------------------------------------
        InvalidTheta = True
        phi = 180

        # TODO - not ideal movements possible
        while InvalidTheta:
            try:
                l1 = self.arm1.length
                l2 = self.arm2.length
                l3 = self.arm3.length

                px = brush_x
                py = brush_y

                px = brush_x - self.arm1.origin[0]
                py = (brush_y - self.arm1.origin[1]) * -1

                phi = np.deg2rad(phi)

                wx = px - l3 * m.cos(phi)
                wy = py - l3 * m.sin(phi)

                delta = (wx) ** 2 + (wy) ** 2
                c2 = (delta - l1 ** 2 - l2 ** 2) / (2 * l1 * l2)
                s2 = m.sqrt(1 - c2 ** 2) 
                theta_2 = np.arctan2(s2, c2)

                s1 = ((l1 + l2 * c2) * wy - l2 * s2 * wx) / delta
                c1 = ((l1 + l2 * c2) * wx + l2 * s2 * wy) / delta
                theta_1 = np.arctan2(s1, c1)
                theta_3 = phi - theta_1 - theta_2

                # print('theta_1: ', np.rad2deg(theta_1))
                # print('theta_2: ', np.rad2deg(theta_2))
                # print('theta_3: ', np.rad2deg(theta_3))

                InvalidTheta = False

            except Exception as e:
                InvalidTheta = True
                phi = np.rad2deg(phi)
                phi += 1

        theta_1 = np.rad2deg(theta_1)
        theta_2 = np.rad2deg(theta_2)
        theta_3 = np.rad2deg(theta_3)

        return -theta_1, -theta_2, -theta_3


window = tk.Tk()

cw = tk.PhotoImage(file="cw.gif")
ccw = tk.PhotoImage(file="ccw.gif")
paintImg = tk.PhotoImage(file="paint.gif")
upImg = tk.PhotoImage(file="up.png")
upImg = upImg.subsample(7, 7)
downImg = tk.PhotoImage(file="down.png")
downImg = downImg.subsample(7, 7)
leftImg = tk.PhotoImage(file="left.png")
leftImg = leftImg.subsample(7, 7)
rightImg = tk.PhotoImage(file="right.png")
rightImg = rightImg.subsample(7, 7)

leftBox = tk.Frame(window)
leftBox.pack(side=tk.LEFT)
rightBox = tk.Frame(window)
rightBox.pack(side=tk.RIGHT)

top = tk.Frame(window)
mid = tk.Frame(window)
bottom = tk.Frame(window)
paint = tk.Frame(window)
top.pack(in_=rightBox, side=tk.TOP)
mid.pack(in_=rightBox, side=tk.TOP)
bottom.pack(in_=rightBox, side=tk.TOP)
paint.pack(in_=rightBox, side=tk.TOP)

lower = tk.Frame(window)
evenLower = tk.Frame(window)
lower.pack(in_=rightBox, side=tk.TOP)
evenLower.pack(in_=rightBox, side=tk.TOP)

# -----------
canvas = tk.Canvas(window, width=800, height=600, bg="white")
canvas.pack(in_=leftBox, pady=20)

# our robot's name is tim!
tim = Robot(canvas)

button1 = tk.Button(window, image=cw, command=tim.arm3CW, repeatdelay=25, repeatinterval=5)
button1.pack(in_=top, side=tk.LEFT)
button2 = tk.Button(window, image=ccw, command=tim.arm3CCW, repeatdelay=25, repeatinterval=5)
button2.pack(in_=top, side=tk.LEFT)
button3 = tk.Button(window, image=cw, command=tim.arm2CW, repeatdelay=25, repeatinterval=5)
button3.pack(in_=mid, side=tk.LEFT)
button4 = tk.Button(window, image=ccw, command=tim.arm2CCW, repeatdelay=25, repeatinterval=5)
button4.pack(in_=mid, side=tk.LEFT)
button5 = tk.Button(window, image=cw, command=tim.arm1CW, repeatdelay=25, repeatinterval=5)
button5.pack(in_=bottom, side=tk.LEFT)
button6 = tk.Button(window, image=ccw, command=tim.arm1CCW, repeatdelay=25, repeatinterval=5)
button6.pack(in_=bottom, side=tk.LEFT)
button7 = tk.Button(window, image=paintImg, command=tim.togglePaint)
button7.pack(in_=paint, side=tk.LEFT)
button8 = tk.Button(window, image=leftImg, command=tim.left, repeatdelay=5, repeatinterval=25)  # made slower
button8.pack(in_=lower, side=tk.LEFT)
button9 = tk.Button(window, image=rightImg, command=tim.right, repeatdelay=5, repeatinterval=25)
button9.pack(in_=lower, side=tk.LEFT)
button10 = tk.Button(window, image=upImg, command=tim.up, repeatdelay=5, repeatinterval=25)
button10.pack(in_=evenLower, side=tk.LEFT)
button11 = tk.Button(window, image=downImg, command=tim.down, repeatdelay=5, repeatinterval=25)
button11.pack(in_=evenLower, side=tk.LEFT)

window.bind('w', tim.up)
window.bind('a', tim.left)
window.bind('s', tim.down)
window.bind('d', tim.right)

window.bind('i', tim.arm1CW)
window.bind('u', tim.arm1CCW)
window.bind('k', tim.arm2CW)
window.bind('j', tim.arm2CCW)
window.bind('m', tim.arm3CW)
window.bind('n', tim.arm3CCW)

window.bind('p', tim.togglePaint)

window.mainloop()
