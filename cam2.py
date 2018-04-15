import cv2
from PIL import Image
import math


class Calculator:
    def __init__(self, gray=None):
        self.gray = gray
        self.binary = None
        self.paper_vertices = None
        self.line_vertices = None
        self.triangle_vertices = None

    def save(self, thresh, name):
        image = Image.fromarray(thresh)
        image.save(name)

    def extract_paper_corners(self):
        # RETR_EXTERNAL - get the contour of the external figure (paper)
        # CHAIN_APPROX_SIMPLE - get only pixels of vertices rather than all figure
        image, contours, hierarchy = cv2.findContours(self.binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # get the first and, hopefully, the only contour
        cnt = contours[0]
        # find the minimum rectangle that covers figure
        x, y, w, h = cv2.boundingRect(cnt)
        # the minimum distance between vertices
        epsilon = min(h, w) * 0.5
        # get only 4 dots of the vertices
        vertices = cv2.approxPolyDP(cnt, epsilon, True)
        # sort in the clockwise order
        vertices = cv2.convexHull(vertices, clockwise=True)
        result = []
        for outer in vertices:
            result.append(tuple(outer[0]))
        self.paper_vertices = result
        return result

    def extract_line_corners(self):
        image, contours, hierarchy = cv2.findContours(self.binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for c in contours:
            # approximate the contour
            x, y, w, h = cv2.boundingRect(c)

            epsilon = max(h, w) * 0.5
            approx = cv2.approxPolyDP(c, epsilon, True)

            if len(approx) != 2:
                continue
            vertices = cv2.convexHull(approx, clockwise=True)
            result = []
            for outer in vertices:
                result.append(tuple(outer[0]))
            return result

    def extract_triangle_corners(self):
        image, contours, hierarchy = cv2.findContours(self.binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for c in contours:
            # approximate the contour
            x, y, w, h = cv2.boundingRect(c)

            epsilon = max(h, w) * 0.2
            approx = cv2.approxPolyDP(c, epsilon, True)

            if len(approx) != 3:
                continue
            vertices = cv2.convexHull(approx, clockwise=True)
            result = []
            for outer in vertices:
                result.append(tuple(outer[0]))
            return result

    def line_length(self, vertices):
        a4_height = 29.7
        a4_width = 21.0
        height_pixels = math.fabs((self.paper_vertices[0][1] + self.paper_vertices[3][1]) / 2.0
                                  - (self.paper_vertices[1][1] + self.paper_vertices[2][1]) / 2.0)
        width_pixels = math.fabs((self.paper_vertices[0][0] + self.paper_vertices[1][0]) / 2.0
                                 - (self.paper_vertices[2][0] + self.paper_vertices[3][0]) / 2.0)
        h_scale = a4_height / height_pixels
        w_scale = a4_width / width_pixels

        print('h_pixels = {} w_pixels = {} h_scale = {} w_scale = {}'.format(height_pixels, width_pixels, h_scale,
                                                                             w_scale))
        return math.sqrt(
            ((vertices[0][0] - vertices[1][0]) * w_scale) ** 2 + ((vertices[0][1] - vertices[1][1]) * h_scale) ** 2)

    def triangle_perimeter(self):
        return self.line_length(self.triangle_vertices[0:2]) + self.line_length(self.triangle_vertices[1:3]) \
               + self.line_length([self.triangle_vertices[0], self.triangle_vertices[2]])

    def triangle_area(self):
        a = self.line_length(self.triangle_vertices[0:2])
        b = self.line_length(self.triangle_vertices[1:3])
        c = self.line_length([self.triangle_vertices[0], self.triangle_vertices[2]])
        p = (a + b + c) / 2
        return math.sqrt(p * (p - a) * (p - b) * (p - c))

    def get_binary_image(self, threshold=127):
        img = cv2.GaussianBlur(self.gray, (5, 5), 0)
        ret, thresh = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
        self.save(thresh, "binary.jpg")
        self.binary = thresh
        return thresh

    def calculate(self):
        if self.gray is None:
            self.gray = cv2.imread('capture.jpg', 0)
        self.get_binary_image()

        self.extract_paper_corners()
        print('[INFO] paper = {}'.format(self.paper_vertices))
        self.extract_line_corners()
        print('[INFO] Line = {}'.format(self.line_vertices))
        self.extract_triangle_corners()
        print('[INFO] triangle = {}'.format(self.triangle_vertices))
