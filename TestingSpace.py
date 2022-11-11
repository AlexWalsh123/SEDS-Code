
from scipy.spatial.transform import Rotation as R #used for rotations 

angle = R.from_euler('z', 90, degrees=True)

angle = angle * R.from_euler('z', -90, degrees=True)
angle = angle * R.from_euler('z', 90, degrees=True)

print(angle.as_quat())