#!/usr/bin/env python

import sys

import rospy

import baxter_interface

from geometry_msgs.msg import (
    PoseStamped,
    Pose,
    Point,
    Quaternion,
)
from std_msgs.msg import Header

from baxter_core_msgs.srv import (
    SolvePositionIK,
    SolvePositionIKRequest,
)

class BasicMove():
	def __init__(self, limb):
		self._limb = baxter_interface.limb.Limb(limb) 

		self._ik_srv = "ExternalTools/" + limb + "/PositionKinematicsNode/IKService"
		self._iksvc = rospy.ServiceProxy(self._ik_srv, SolvePositionIK)
		self._ikreq = SolvePositionIKRequest()

		# Verify robot is enabled
		print "Getting robot state..."
		self._rs = baxter_interface.RobotEnable()
		self._init_state = self._rs.state().enabled
		print "Enabling robot..."
		self._rs.enable()
		print "Running. Ctrl-c to quit"

	def _find_jp(self, position):
		self._ikreq.pose_stamp.append(position)
		
		try:
			rospy.wait_for_service(self._ik_srv, 5.0)
			resp = self._iksvc(self._ikreq)
			if resp.isValid[0]:
				print "SUCCESS - Valid Joint Solution Found"
				# Format solution into Limb API-compatible dictionary
				limb_joints = dict(zip(resp.joints[0].name, resp.joints[0].position))
				return limb_joints
			else:
				print "INVALID POSE - No Valid Joint Solution Found."
				return False
		except (rospy.ServiceException, rospy.ROSException), e:
			rospy.logerr("Service call failed: %s" % (e,))
			return False
	
	def set_neutral(self):
		self._limb.move_to_neutral()

	def move_to_coords(self, pose):
		limb_joints = self._find_jp(pose)
		#print limb_joints
		if limb_joints != False:
			self._limb.move_to_joint_positions(limb_joints)
			return True
		else:
			return False

	def move_to_jp(self, position):
		self._limb.move_to_joint_positions(position) 

	def clean_shutdown(self):
		print "\nExiting basic poke..."
		self._limb.exit_control_mode()
		if not self._init_state and self._rs.state().enabled:
			print "Disabling robot..."
			self._rs.disable()
		
def main():
	rospy.init_node("cs473_basic_poke")

	bm = BasicMove('right')

	# register shutdown callback
	rospy.on_shutdown(bm.clean_shutdown)

	print "Moving to neutral pose..."
	bm.set_neutral()

	# Hard-coded pose
	hdr = Header(stamp=rospy.Time.now(), frame_id='base')
	poses = {
		'right': PoseStamped(
			header=hdr,
	   		pose=Pose(
	       		position=Point(
	           		x=0.656982770038,
	           		y=-0.852598021641,
	           		z=0.0388609422173,
	       		),
	       		orientation=Quaternion(
	           		x=0.367048116303,
	           		y=0.885911751787,
	           		z=-0.108908281936,
	           		w=0.261868353356,
	       		),
	   		),
		),
	}
	print "Moving to pose specified by coordinates..."
	bm.move_to_coords(poses['right'])

	initial = {
		'right_s0': 0.573325318817, 
		'right_s1': -0.268063142377, 
		'right_w0': -0.125786424463, 
		'right_w1': -1.48872835294, 
		'right_w2': -0.299509748492, 
		'right_e0': 0.322135965088, 
		'right_e1': 1.90060219402
	}
	print "Moving to pose specified by joint positions..."
	bm.move_to_jp(initial)
	

if __name__ == '__main__':
	main() 