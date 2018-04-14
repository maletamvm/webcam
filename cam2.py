import numpy as np
import cv2
from PIL import Image, ImageDraw
import math


def takePhoto():
    cap = cv2.VideoCapture(0)

    while (True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Display the resulting frame
        cv2.imshow('frame', gray)
        if cv2.waitKey(1) & 0xFF == ord('e'):
            cv2.imwrite('capture.jpg', gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


def save(thresh, name):
    image = Image.fromarray(thresh)
    image.save(name)


def extract_paper_corners(thresh):
    # RETR_EXTERNAL - get the contour of the external figure (paper)
    # CHAIN_APPROX_SIMPLE - get only pixels of vertices rather than all figure
    image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

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
    return result


def extract_line_corners(thresh):
    image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

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


def extract_triangle_corners(thresh):
    image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

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


def line_length (vertices, paper):
    a4_height = 29.7
    a4_width = 21.0
    height_pixels = math.fabs((paper[0][1] + paper[3][1]) / 2.0 - (paper[1][1] + paper[2][1]) / 2.0)
    width_pixels = math.fabs((paper[0][0] + paper[1][0]) / 2.0 - (paper[2][0] + paper[3][0]) / 2.0)
    h_scale = a4_height / height_pixels
    w_scale = a4_width / width_pixels

    print('h_pixels = {} w_pixels = {} h_scale = {} w_scale = {}'.format(height_pixels, width_pixels, h_scale, w_scale))
    return math.sqrt(((vertices[0][0] - vertices[1][0]) * w_scale) ** 2 + ((vertices[0][1] - vertices[1][1]) * h_scale) ** 2)


def triangle_perimeter (vertices, paper):
    return line_length(vertices[0:2], paper) + line_length(vertices[1:3], paper) + line_length([vertices[0], vertices[2]], paper)


def triangle_area (vertices, paper):
    a = line_length(vertices[0:2], paper)
    b = line_length(vertices[1:3], paper)
    c = line_length([vertices[0], vertices[2]], paper)
    p = (a + b + c) / 2
    return math.sqrt(p * (p - a) * (p - b) * (p - c))


def get_binary_image(img, threshold = 127):
    img = cv2.GaussianBlur(img, (5, 5), 0)
    ret, thresh = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
    save(thresh, "binary1.jpg")
    return thresh


takePhoto()
img = cv2.imread('capture.jpg', 0)
thresh = get_binary_image(img)
save (thresh, "binary1.jpg")

paper_vertices = extract_paper_corners(thresh)
print('paper = {}'.format(paper_vertices))
line_vertices = extract_line_corners(thresh)
print('Line = {}'.format(line_vertices))
triangle_vertices = extract_triangle_corners(thresh)
print('triangle = {}'.format(triangle_vertices))

print('Line length = {}'.format(line_length(line_vertices, paper_vertices)))

# image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# img = cv2.imread('triangle.jpg', 0)
# i=0
# save(img, "result0.jpg")
#
# for c in contours:
#     i += 1
#     cv2.drawContours(img, [c], 0, (255, 255, 255), 3)
#     image_binary = Image.fromarray(img)
#     image_binary.save("result{}.jpg".format(i), "JPEG")