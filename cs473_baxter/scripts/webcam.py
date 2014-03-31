#!/usr/bin/python

import time
import sys
import os

import cv2

import rospy

class Webcam():
	def __init__(self, img_dir):
		self.device = 0 # assume we want first device
		print "Opening capture device..."
		self.capture = cv2.VideoCapture(self.device)
		self.capture.set(3,960) # CV_CAP_PROP_FRAME_WIDTH  
		self.capture.set(4,720) # CV_CAP_PROP_FRAME_HEIGHT 
		self.img_dir = img_dir

		if not self.capture:
			print "Error opening capture device"
			sys.exit(1)

	def show_video_stream(self):
		while True:
			val, frame = self.capture.read()
			cv2.imshow("input", frame)

			key = cv2.waitKey(50) % 256
			if key == ord('q'):
				break
			
	def take_snapshot(self, file_name):
		while True:
			val, frame = self.capture.read()
			cv2.imshow("input", frame)

			key = cv2.waitKey(50) % 256
			if key == ord('q'):
				print "Taking snapshot cancelled."
				break
			else if key == ord(' '):
				print "Taking snapshot..."
				cv2.imwrite(os.path.join(self.img_dir, file_name), frame)
				print "Image saved."
				break

	def take_reference_snapshot(self):
		print "Taking snapshot of background."
		val, frame = self.capture.read()
		cv2.imwrite(os.path.join(self.img_dir, "background.jpg"), frame)
		print "Image saved."
		
		print "Place box in center. Press SPACE when finished."
		self.take_snapshot("box.jpg")
		
		print "Remove box and move arm into view. Press SPACE when finished."
		self.take_snapshot("arm.jpg")
		
	def take_uncompressed_snapshot(self):
		print "Place object alone in center. Press SPACE when finished."
		self.take_snapshot("object.jpg")
		
	def take_compressed_snapshot(self):
		print "Compress object with arm. Press SPACE when finished."
		self.take_snapshot("object.jpg")

def main():
	img_dir = "./src/cs473-baxter-project/cs473_baxter/images/"
	w = Webcam(img_dir)
	w.show_video_stream()
	time.sleep(10)
	w.take_snapshots()


if __name__ == '__main__':
	main()
