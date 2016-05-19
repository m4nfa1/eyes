import numpy as np
import cv2
import imutils
import matplotlib.pyplot as plt
import glob
import os

class Searcher:
	def __init__(self, imageLink):
		self.imageLink = imageLink

	def search(self):
		if self.imageLink:
			img1 = cv2.imread(self.imageLink)
			img1 = imutils.resize(img1, width=1000)
			img1 = cv2.cvtColor(img1, cv2.COLOR_RGBA2GRAY)
			surf = cv2.xfeatures2d.SURF_create(2000,7,7)

			kp1, des1 = surf.detectAndCompute(img1, None)

			ans = {}

			for imagePath in glob.glob("logo/**/*.png"):
				img2 = cv2.imread(imagePath)
				img2 = cv2.cvtColor(img2, cv2.COLOR_RGBA2GRAY)
				img2 = imutils.resize(img2, width=500)
				kp2, des2 = surf.detectAndCompute(img2, None)
				bf = cv2.BFMatcher()
				matches = bf.knnMatch(des2, des1, k=2)
				good = []
				for m,n in matches:
				    if m.distance < 0.7*n.distance:
				        good.append([m])
				percent = len(good)
				ans.update({imagePath:percent})
				percent = str(round(percent, 2))
				img3 = cv2.drawMatchesKnn(img2, kp2, img1, kp1, good, None, flags=2)
				cv2.putText(img3, ("Good: " + str(len(good))), (10,400), 0, 1, (0,0,255),2)
				cv2.imwrite("static/result/" + str(os.path.basename(imagePath)), img3)

		if max(ans.values()) >= 20:
			result = str(max(ans, key=ans.get))
		else:
			result = 'UNKNOWN'
		return result


