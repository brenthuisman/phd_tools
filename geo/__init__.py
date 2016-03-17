import ROOT as r,math

def rotator(heading, attitude, bank):
	#Converts from euler angles to matrix angles (or something like that, I'm not even sure.)
	#src:
	#http://proj-clhep.web.cern.ch/proj-clhep/doc/CLHEP_2_1_3_1/doxygen/html/Rotation_8cc-source.html#l00153
	#Gate and Geant4 rotations actually are typedefd CLHEP rotations.
	#http://www.euclideanspace.com/maths/geometry/rotations/conversions/eulerToMatrix/index.htm

	ch = math.cos(heading)
	sh = math.sin(heading)
	ca = math.cos(attitude)
	sa = math.sin(attitude)
	cb = math.cos(bank)
	sb = math.sin(bank)
	m00 = ch * ca
	m01 = sh*sb - ch*sa*cb
	m02 = ch*sa*sb + sh*cb
	m10 = sa
	m11 = ca*cb
	m12 = -ca*sb
	m20 = -sh*ca
	m21 = sh*sa*cb + ch*sb
	m22 = -sh*sa*sb + ch*cb

	cosa  = 0.5*(m00+m11+m22-1)
	cosa1 = 1-cosa
	angle=[]
	aaxis=[]
	if (cosa1 <= 0):
		angle = [0]
		aaxis = [0,0,1]
	else:
		x=0
		y=0
		z=0
		if (m00 > cosa): x = math.sqrt((m00-cosa)/cosa1)
		if (m11 > cosa): y = math.sqrt((m11-cosa)/cosa1)
		if (m22 > cosa): z = math.sqrt((m22-cosa)/cosa1)
		if (m21 < m12): x = -x
		if (m02 < m20): y = -y
		if (m10 < m01): z = -z
		#angle = (cosa < -1.) ? std::acos(-1.) : std::acos(cosa);
		#angle = (cosa < -1.) ? math.acos(-1.) : math.acos(cosa)
		if cosa < -1.:
			angle = [math.acos(-1.)]
		else:
			angle = [math.acos(cosa)]
		aaxis = [x,y,z]
	angle[0]=math.degrees(angle[0])
	angle.extend(aaxis)
	return angle

