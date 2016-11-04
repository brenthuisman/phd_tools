class rtplan:
	def __init__(self,filename, **kwargs):
		#defaults
		self.nprims=4e10
		self.edep=True
		self.MSW_to_protons=True
		
		for key in ('nprims', 'edep', 'MSW_to_protons', 'killzero'):
			if key in kwargs:
				setattr(self, key, kwargs[key])
		
		self.TotalMetersetWeight = 0.
		self.layers = []
		self.spots = []
		self.metadata = []
		self.layerhistrange = []
		self.rangetable = []
		self.nrfields = 0
		self.fieldids = []
		
		sourcefile = open(filename,'r')
	
		capture_NbOfScannedSpots = 0
		capture_Spots = 0
		capture_CumulativeMetersetWeight = 0
		capture_TotalMetersetWeight = 0
		capture_Energy = 0
		capture_Energy_first = 1
		capture_FieldID = 0
		capture_ControlPointIndex = 0
		capture_GantryAngle = 0

		previous_CumulativeMetersetWeight = 0
		CumulativeMetersetWeight = 0
		MSWfactor = 0
		Energy = 0
		Energy_first = 0
		Energy_last = 0
		NbOfScannedSpots = 0
		FieldID = 0
		ControlPointIndex = 0
		GantryAngle = 0

		for index, line in enumerate(sourcefile):
			newline = line.strip()
			if len(newline)==0:
				continue
		
			if newline[0] == "#":
				#we are reading a fieldname
				#stop reading spots if we were doing that.
				capture_Spots = 0
				newline = newline.replace('#','')
				if newline == 'CumulativeMetersetWeight':
					#if the field is CumulativeMetersetWeight,
					#we're engaging capture mode because next we'll get
					#energy and number of spots, and thus we can 
					#calculate fluence.
					capture_CumulativeMetersetWeight = 1
					continue
	
				if newline == 'Energy (MeV)':
					capture_Energy = 1
					continue
	
				if newline == 'TotalMetersetWeightOfAllFields':
					capture_TotalMetersetWeight = 1
					continue
	
				if newline == 'NbOfScannedSpots':
					capture_NbOfScannedSpots = 1
					continue
			
				if newline == 'GantryAngle':
					#new field ==  new dataset
					capture_GantryAngle = 1
					continue
			
				if newline == 'FieldID':
					#new field ==  new dataset
					# fieldID doesnt have to be incremental!
					self.nrfields += 1
					capture_FieldID = 1
					continue
			
				if newline == 'ControlPointIndex':
					capture_ControlPointIndex = 1
					continue
				
				if newline == 'X Y Weight':
					capture_Spots = 1
					continue

			if capture_ControlPointIndex == 1:
				#CPI in rtplan starts at 0
				ControlPointIndex = int(newline)
				capture_ControlPointIndex = 0
		
			if capture_GantryAngle == 1:
				GantryAngle = int(newline)
				capture_GantryAngle = 0
		
			if capture_CumulativeMetersetWeight == 1:
				#Note: CumulativeMetersetWeight is the amount of dose/fluence delivered so far.
				#It does NOT!!!! include the dose/fluence in this particular controlpoint.
				#Note2: CPIs are grouped in pairs: the first defines the weights per spot, the second the total CMW.
				new_CumulativeMetersetWeight = float(newline)
				if new_CumulativeMetersetWeight == 0:
					#If it's 0, we are at the start of a new Field.
					CumulativeMetersetWeight = 0
					previous_CumulativeMetersetWeight = 0
					capture_CumulativeMetersetWeight = 0
					continue
				else:
					#Can this happen?
					previous_CumulativeMetersetWeight = CumulativeMetersetWeight
					CumulativeMetersetWeight = new_CumulativeMetersetWeight
					capture_CumulativeMetersetWeight = 0

			if capture_FieldID == 1:
				#Field in rtplan starts at 1.
				FieldID = int(newline)
				self.fieldids.append(FieldID)
				capture_FieldID = 0
		
			if capture_Energy == 1:
				capture_Energy = 0
				new_Energy = float(newline)
				if new_Energy == 0:
					#end of the Field, we still have to record the CMW though!!!!
					capture_Energy_first = 1
					Energy_last = Energy
					Energy = new_Energy
					continue
				Energy = new_Energy
				if capture_Energy_first == 1:
					Energy_first = new_Energy
					capture_Energy_first = 0

			if capture_TotalMetersetWeight == 1:
				#it appears the sums never are really quite correct, so we'll set later if and when converted to nb_prots
				self.TotalMetersetWeight = float(newline)
				capture_TotalMetersetWeight = 0
		
			if capture_NbOfScannedSpots == 1:
				capture_NbOfScannedSpots = 0
				if CumulativeMetersetWeight == previous_CumulativeMetersetWeight:
					#First CPI of the energylayer, so just set the value and be done.
					NbOfScannedSpots = int(newline)
					continue
				if Energy == 0:
					#End of the field, here NbOfScannedSpots = int(newline) = 0, so dont overwrite.
					self.layers.append([FieldID,Energy_last,(CumulativeMetersetWeight-previous_CumulativeMetersetWeight),NbOfScannedSpots])
					self.metadata.append([FieldID,(ControlPointIndex)/2+1,Energy_first,Energy_last,CumulativeMetersetWeight,GantryAngle])
				else:
					NbOfScannedSpots = int(newline)
					self.layers.append([FieldID,Energy,(CumulativeMetersetWeight-previous_CumulativeMetersetWeight),NbOfScannedSpots])
					
			if capture_Spots == 1:
				#Only capture spots for first of pairs of CMWs
				if CumulativeMetersetWeight == previous_CumulativeMetersetWeight:
					x,y,weight = newline.split(' ')
					if self.killzero and float(weight) == 0:
						continue
					self.spots.append([FieldID,Energy,float(x),float(y),float(weight)])
				#Because Spots are multiline, we stop it when handling lines starting with '#', see top of function.
		
	
		sourcefile.close()
		#self.nrfields=self.metadata[-1][0]
		self.autolayerhistrange()
		self.autospothistrange()
		if self.MSW_to_protons == True:
			self.msw_to_prot()


	def autolayerhistrange(self):
		#find high and low points for histograms
		#TODO can I do without this? can the edges for a TH1D be changed afterwards?
		low = 1000000 #1TeV seems like a fine upperlimit
		high = 0
		for entry in self.metadata:
			low = min(low,entry[2],entry[3])
			high = max(high,entry[2],entry[3])
	
		#Make sure the upper and lower bins are within view.
		low-=1
		high+=1
		self.layerhistrange=[low,high]


	def autospothistrange(self):
		#find high and low points for histograms
		#TODO can I do without this? can the edges for a TH1D be changed afterwards?
		low = 0 #0 is the lowest, obviously
		high = 0
		for entry in self.spots:
			high = max(high,entry[-1])
	
		#Make sure the upper and lower bins are within view doesnt seem necesary.
		#low-=1
		#high+=1
		self.spothistrange=[low,high]


	def getlayerdata(self, layerhistrange=None):
		if layerhistrange is not None:
			self.layerhistrange = layerhistrange

		#array of data
		histos=[]
		
		# Create some histograms
		for i in range(self.nrfields):
			curfieldid = self.fieldids[i]
			xv=[]
			yv=[]
			for cp in self.layers:
				if cp[0] == curfieldid:
					xv.append(cp[1]) #energy
					yv.append(cp[2]) #nbprots
			histos.append([xv,yv])
		
		return histos


	def getspotdata(self, spothistrange=None):
		if spothistrange is not None:
			self.spothistrange = spothistrange

		#array of data, not really a histo
		histos=[]
		
		# Create some histograms

		for i in range(self.nrfields):
			curfieldid = self.fieldids[i]
			xv=[]
			yv=[]
			for spot in self.spots:
				if spot[0] == curfieldid:
					xv.append(spot[1]) #energy
					yv.append(spot[-1]) #nbprots
			histos.append([xv,yv])
		
		return histos


	def ConvertMuToProtons(self,weight,energy):
		#straight from GateSourceTPSPencilBeam, seems to introduce small energy-dep on #prots/MU
		K=37.60933
		SP=9.6139E-09 * energy**4 - 7.0508E-06 * energy**3 + 2.0028E-03 * energy**2 - 2.7615E-01 * energy**1 + 2.0082E+01 * energy**0
		PTP=1.
		Gain=3./(K*SP*PTP*1.602176E-10)
		return weight*Gain
	

	def msw_to_prot(self):
		#to verify that TPSes don't compute the correct MSW sums, we record laysum, spotsum. IN SPOT WE TRUST
		spotsum = 0.
		laysum = [0.]*self.nrfields
		for i,field in enumerate(self.metadata):
			laysum[i] = field[4]
		for spot in self.spots:
			spotsum += spot[4]
		
		print sum(laysum),self.TotalMetersetWeight,spotsum
		
		#since its not linear, we must twopass
		if self.edep == True:
			spotsum = 0.
			#first pass: update MSWs
			#laysum = [0.]*self.nrfields #we recompute based on new weights
			for layer in self.layers:
				E = layer[1]
				MSW = layer[2]
				layer[2] = self.ConvertMuToProtons(MSW, E)
				laysum[layer[0]-1] += layer[2]
			for spot in self.spots:
				E = spot[1]
				MSW = spot[4]
				spot[4] = self.ConvertMuToProtons(MSW, E)
				spotsum += spot[4]
			for i,field in enumerate(self.metadata):
				field[4] = laysum[i]
			self.TotalMetersetWeight = sum(laysum)
		
		print sum(laysum),self.TotalMetersetWeight,spotsum
		
		#convert MSW to nprims. linear.
		#MSWfactor = self.nprims/self.TotalMetersetWeight #so this gives a slightly wrong number of protons.
		MSWfactor = self.nprims/spotsum
		laysum = [0.]*self.nrfields #we recompute
		spotsum = 0.
		for layer in self.layers:
			layer[2] *= MSWfactor
			laysum[layer[0]-1] += layer[2]
		for spot in self.spots:
			spot[4] *= MSWfactor
			spotsum += spot[4]
		for field in self.metadata:
			field[4] *= MSWfactor
		self.TotalMetersetWeight *= MSWfactor
		
		print sum(laysum),self.TotalMetersetWeight,spotsum
		
		#if you had enabled the print statements, you saw that sum(spots) is not sum(layers) is not TotalMetersetWeight.
		#so lets recalc layers and TotalMetersetWeight based on spot weights.
		for layer in self.layers:
			layer[2] = 0.
		for field in self.metadata:
			field[4] = 0.
		laysum = [0.]*self.nrfields
		for spot in self.spots:
			fieldid = spot[0]
			E = spot[1]
			spotWeight = spot[4]
			for layer in self.layers:
				if layer[0] == fieldid and layer[1] == E:
					layer[2] += spotWeight
					laysum[layer[0]-1] += spotWeight
		for i,field in enumerate(self.metadata):
			field[4] = laysum[i]
		self.TotalMetersetWeight = sum(laysum)
		
		print sum(laysum),self.TotalMetersetWeight,spotsum
		
		print "Conversion to correct numbers of protons complete."
