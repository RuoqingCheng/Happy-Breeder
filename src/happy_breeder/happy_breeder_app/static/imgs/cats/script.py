import cv2
import numpy as np
import os

def add(img1, img2, x, y):
	new_x = max(x + img2.shape[0], img1.shape[0])
	new_y = max(y + img2.shape[0], img1.shape[1])
	new_img = np.zeros((new_x, new_y, 4))
	new_img[0:img1.shape[0], 0:img1.shape[1]] = img1

	for i in range(img2.shape[0]):
		for j in range(img2.shape[1]):
			if x + i < img1.shape[0] and y + j < img1.shape[1]:
				alpha1 = img1[x + i, y + j, 3] / 255
				alpha2 = img2[i, j, 3] / 255
				alpha = alpha1 + alpha2 - alpha1 * alpha2
				new_img[x + i, y + j, 0:3] = (img1[x + i, y + j, 0:3] * alpha1 * (1 - alpha2) + img2[i, j, 0:3] * alpha2) / alpha
				new_img[x + i, y + j, 3] = alpha * 255
			else:
				new_img[x + i, y + j] = img2[i, j]

	return new_img

def enlarge_wing(img):
	new_img = np.zeros((img.shape[0] + 30, img.shape[1], 4))
	new_img[30:30 + img.shape[0]] = img
	return new_img

# def enlarge_wing(img):
# 	new_img = np.zeros((360, img.shape[1], 4))
# 	new_img[160:160 + img.shape[1]] = img
# 	return new_img

def add_eye(types, body, eyeL, eyeR):
	sche = {"B1": [(88, 70), (88, 165)], "B2": [(88, 70), (88, 165)], "B3": [(118, 70), (118, 165)], "B4": [(98, 70), (98, 165)], "B5": [(93, 70), (93, 165)]}
	new_img = add(body, eyeL, sche[types][0][0], sche[types][0][1])
	new_img = add(new_img, eyeR, sche[types][1][0], sche[types][1][1])
	return new_img

def add_wing(types, body, wing):
	new_img = add(wing, body, 0, 34)
	return new_img

def add_leg(types, body, leg):
	sche = {"B1": (290, 112), "B2": (290, 112), "B3": (320, 112), "B4": (290, 112), "B5": (290, 112)}
	new_img = add(body, leg, sche[types][0], sche[types][1])
	return new_img

# w1 = cv2.imread("./wing/W1.png", -1)
# w2 = cv2.imread("./wing/W2.png", -1)
# w3 = cv2.imread("./wing/W3.png", -1)
# w4 = cv2.imread("./wing/W4.png", -1)
# cv2.imwrite("./wing/W3_alter.png", enlarge_wing(w3))
# cv2.imwrite("./wing/W4_alter.png", enlarge_wing(w4))
# w1a = cv2.imread("./wing/W1_alter.png", -1)
# w2a = cv2.imread("./wing/W2_alter.png", -1)
# w3a = cv2.imread("./wing/W3_alter.png", -1)
# w4a = cv2.imread("./wing/W4_alter.png", -1)

# b1 = cv2.imread('./body/B1.png', -1)
# b2 = cv2.imread('./body/B2.png', -1)
# b3 = cv2.imread('./body/B3.png', -1)
# b4 = cv2.imread('./body/B4.png', -1)
# b5 = cv2.imread('./body/B5.png', -1)
# e1 = cv2.imread('./eye/LR1.png', -1)
# e2 = cv2.imread('./eye/LR2.png', -1)
# e3 = cv2.imread('./eye/LR3.png', -1)
# e4 = cv2.imread('./eye/LR4.png', -1)
# e5 = cv2.imread('./eye/LR5.png', -1)

# body = [b1, b2, b3, b4, b5]
# eye = [e1, e2, e3, e4, e5]
# wing = [(w1, w1a), (w2, w2a), (w3, w3a), (w4, w4a)]
# img2 = cv2.imread('./body/B1.png', -1)

# img1 = add(img1, img2, 0, 34)

# cv2.imwrite("./wing/W1_alter.png", enlarge_wing(w1))
# cv2.imwrite("./wing/W2_alter.png", enlarge_wing(w2))
# cv2.imwrite("./wing/W3_alter.png", enlarge_wing(w3))
# cv2.imwrite("./wing/W4_alter.png", enlarge_wing(w4))

# for i in range(1, len(body) + 1):
# 	for j in range(1, len(eye) + 1):
# 		for k in range(1, len(eye) + 1):
# 			 types = "B" + str(i)
# 			 cv2.imwrite("./L" + str(j) + "R" + str(k) + "B" + str(i) + ".png", add_eye(types, body[i - 1], eye[j - 1], eye[k - 1]))

l1 = cv2.imread('./leg/L1.png', -1)
l2 = cv2.imread('./leg/L2.png', -1)
l3 = cv2.imread('./leg/L3.png', -1)
l4 = cv2.imread('./leg/L4.png', -1)
l5 = cv2.imread('./leg/L5.png', -1)

leg = [l1, l2, l3, l4, l5]

# # cv2.imwrite("./test1.png", add(body, l1, 320, 112))

for root, path, files in os.walk("./new_temp"):
	for file in files:
		temp = file.split(".")
		types = file[4:6]
		body = cv2.imread(root + "/" + file, -1)
		for i in range(len(leg)):
			cv2.imwrite("./" + temp[0] + "S" + str(i + 1) + ".png", add_leg(types, body, leg[i]))
