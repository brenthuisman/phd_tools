import time,ROOT as r,math,tableio

class rtplan:
	def __init__(self,filename,nbprotons=4e10):
		self.layers = []
		self.spots = []
		self.metadata = []
		self.layerhistrange = []
		self.rangetable = []
		
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
				MSWfactor = nbprotons/float(newline)
				capture_TotalMetersetWeight = 0
		
			if capture_NbOfScannedSpots == 1:
				capture_NbOfScannedSpots = 0
				if CumulativeMetersetWeight == previous_CumulativeMetersetWeight:
					#First CPI of the energylayer, so just set the value and be done.
					NbOfScannedSpots = int(newline)
					continue
				if Energy == 0:
					#End of the field, here NbOfScannedSpots = int(newline) = 0, so dont overwrite.
					self.layers.append([FieldID,Energy_last,(CumulativeMetersetWeight-previous_CumulativeMetersetWeight)*MSWfactor,NbOfScannedSpots])
					self.metadata.append([FieldID,(ControlPointIndex)/2+1,Energy_first,Energy_last,CumulativeMetersetWeight*MSWfactor,GantryAngle])
				else:
					NbOfScannedSpots = int(newline)
					self.layers.append([FieldID,Energy,(CumulativeMetersetWeight-previous_CumulativeMetersetWeight)*MSWfactor,NbOfScannedSpots])
					
			if capture_Spots == 1:
				#Only capture spots for first of pairs of CMWs
				if CumulativeMetersetWeight == previous_CumulativeMetersetWeight:
					#Spots.append(float(newline.split(' ')[-1]))
					self.spots.append([FieldID,Energy,float(newline.split(' ')[0]),float(newline.split(' ')[1]),float(newline.split(' ')[2])*MSWfactor])
				#Because Spots are multiline, we stop it when handling lines starting with '#', see top of function.
		
	
		sourcefile.close()
		self.autolayerhistrange()
		self.autospothistrange()


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

	def getlayerhistos(self, nrbins=100, layerhistrange=None):
		if layerhistrange is not None:
			self.layerhistrange = layerhistrange
		#make more readable
		nrFields = self.metadata[-1][0]

		#array of TH1Fs
		histos=[]
		
		# Create some histograms
		for i in range(nrFields):
			title = 'Treatment Plan Energy Structure for Field no'+str(i+1)
			histos.append(r.TH1D( title, title, nrbins, self.layerhistrange[0], self.layerhistrange[1] ))
			for cp in self.layers:
				if cp[0] == i+1:
					histos[-1].Fill(cp[1],cp[2])
			histos[-1].SetTitle(title+";Energy [MeV]"+";Nb. protons")
		
		return histos

	def getspothistos(self, nrbins=100, spothistrange=None):
		if spothistrange is not None:
			self.spothistrange = spothistrange
		#make more readable
		nrFields = self.metadata[-1][0]

		#array of TH1Fs
		histos=[]
		
		# Create some histograms
		for i in range(nrFields):
			title = 'Treatment Plan Spot Structure for Field no'+str(i+1)
			histos.append(r.TH2F( title, title, nrbins, self.layerhistrange[0], self.layerhistrange[1], nrbins, self.spothistrange[0], self.spothistrange[1] ))
			for spot in self.spots:
				if spot[0] == i+1:
					histos[-1].Fill(spot[1],spot[-1])
			histos[-1].SetMarkerStyle(3)
			histos[-1].SetTitle(title+";Energy [MeV]"+";Nb. protons")
		
		return histos

	def setrangetable(self,filename,density=1,headersize=8):
		self.rangetable = tableio.read(filename,headersize)
		for item in self.rangetable:
			item[1]/=float(density)
		#since the density of water is 1, no need to correct right now. for pmma, its different.

	def getrangehistos(self, filename, nrbins=200):
		self.setrangetable(filename)

		# makes it  more readable
		nrFields = self.metadata[-1][0]

		# Create some histograms
		histos=[]
		for i in range(nrFields):
			title = 'Treatment Plan Proton Range in Field no'+str(i+1)
			histos.append(r.TH1D( title, title, nrbins, self.layerhistrange[0], self.layerhistrange[1] ))
			for cp in self.layers:
				if cp[0] == i+1:
					#cp[1] holds an energy, which we must convert to range using the rangetable set.
					#for(j = 0; j < tbl_data.size(); j++){
					depth=0
					for j,jtem in enumerate(self.rangetable):
						if cp[1]<jtem[0]:
							#Superfastfitting: ((x - x-)/(x- - x+))=((y - y-)/(y- - y+)) ; solve for y
							depth = ((cp[1] - self.rangetable[j-1][0])/(self.rangetable[j-1][0] - self.rangetable[j][0]))*(self.rangetable[j-1][1]-self.rangetable[j][1])+self.rangetable[j-1][1]
							#print cp[1], self.rangetable[j-1][0], jtem[0], depth
							break
					#dont forget to convert cm to mm
					histos[i].Fill((depth)*10,cp[2])
		
		return histos

		
	def savelayerhistos(self,nrbins=100,fileformat=".pdf"):
		#functions should eventually move to root_graphing
		histos = self.getlayerhistos(nrbins)
		for i,histo in enumerate(histos):
			title = 'Treatment Plan Energy Structure for Field no'+str(i+1)
			canv = r.TCanvas( title, title )
			histos[i].Draw()
			#See http://root.cern.ch/root/html/TPad.html#TPad:SaveAs for possible output formats.
			canv.SaveAs(fileformat)

	def savespothistos(self,nrbins=100,fileformat=".pdf"):
		#functions should eventually move to root_graphing
		histos = self.getspothistos(nrbins)
		for i,histo in enumerate(histos):
			title = 'Treatment Plan Spot Structure for Field no'+str(i+1)
			canv = r.TCanvas( title, title )
			canv.SetLogy()
			histos[i].Draw()
			#See http://root.cern.ch/root/html/TPad.html#TPad:SaveAs for possible output formats.
			canv.SaveAs(fileformat)

	def showlayerhistos(self,nrbins=100,delay=20):
		#functions should eventually move to root_graphing
		histos = self.getlayerhistos(nrbins)
		canv=[]
		for i,histo in enumerate(histos):
			title = 'Treatment Plan Energy Structure for Field no'+str(i+1)
			canv.append(r.TCanvas( title, title ))
			histos[i].Draw()
	
		time.sleep(delay)

