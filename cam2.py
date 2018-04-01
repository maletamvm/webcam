import numpy as np
import cv2
from PIL import Image, ImageDraw


def takePhoto():
    cap = cv2.VideoCapture(1)

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
    image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cnt = contours[0]
    x, y, w, h = cv2.boundingRect(cnt)
    epsilon = min(h, w) * 0.5
    vertices = cv2.approxPolyDP(cnt, epsilon, True)
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

        epsilon = min(h, w) * 0.5
        approx = cv2.approxPolyDP(c, epsilon, True)

        # if our approximated contour has four points, then
        # we can assume that we have found our screen
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

        # if our approximated contour has four points, then
        # we can assume that we have found our screen
        if len(approx) != 3:
            continue
        vertices = cv2.convexHull(approx, clockwise=True)
        result = []
        for outer in vertices:
            result.append(tuple(outer[0]))
        return result


# takePhoto()
img = cv2.imread('triangle.jpg', 0)
img = cv2.GaussianBlur(img, (5, 5), 0)
ret, thresh = cv2.threshold(img, 191, 255, cv2.THRESH_BINARY)
save (thresh, "binary1.jpg")


paper_vertices = extract_paper_corners(thresh)
print('paper = {}'.format(paper_vertices))
line_vertices = extract_line_corners(thresh)
print('Line = {}'.format(line_vertices))
triangle_vertices = extract_triangle_corners(thresh)
print('triangle = {}'.format(triangle_vertices))

# img = cv2.imread('capture.jpg', 0)
# i=0
# save(img, "result0.jpg")

# for c in contours:
#     i += 1
#     cv2.drawContours(img, [c], 0, (0, 255, 0), 3)
#     image_binary = Image.fromarray(img)
#     image_binary.save("result{}.jpg".format(i), "JPEG")