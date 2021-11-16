import math
class Beam:
    def __init__(self, L, E, I, A, Lcant, Rcant, left_support_type, right_support_type):
        # self beam class assumes there are only two supports for the beam


        # Beam object
        # L = total length
        # E = Modulus of elasticity
        # I = Moment of inertia
        # A = Area
        # Lcant = Left cantilever length
        # Rcant = Right cantilever length
        # self.left_support_restraints = [Vx, Vy, Vz, Mx, My, Mz]
        # where 

        # self.PLs = list of point load objects
        # self.DLs = list of distributed load objects
        # self.POIs = list of distances that are points of interest where cuts will be made to solve for internal forces 

        self.L = L
        self.E = E
        self.I = I
        self.A = A
        self.Lcant = Lcant
        self.Rcant = Rcant
        self.L_btwn_supports = self.L - self.Lcant - self.Rcant
        self.left_support_restraints = left_support_type
        self.left_support_type = right_support_type
        self.PLs = []
        self.DLs = []
        self.POIs = []
        self.maxPL = 0
        self.maxDL = 0

    def defineLoad(self, color, magnitude, startLocation, endLocation=None, endMagnitude=None):
        # determine if point or dist load
        if endLocation:
            load = Dist(color, magnitude, startLocation, endLocation)
            self.DLs.push(load)
            load.index = self.DLs.length-1
            load.type = 'dist'

            if math.abs(load.magnitude) > self.maxDL:
                self.maxDL = math.abs(load.magnitude)
                load.isMaxDL = True

                for item in self.DLs:
                    item.isMaxDL = False

            else:
                load.isMaxDL = False
        
        else:
            load = Point(color, magnitude, startLocation)
            self.PLs.push(load)
            load.index = self.PLs.length-1
            load.type = 'point'

            if math.abs(load.magnitude) > self.maxPL:
                self.maxPL = math.abs(load.magnitude)
                load.isMaxPL = True

                for item in self.PLs:
                    item.isMaxPL = False

            else:
                load.isMaxPL = False
    

    def getBeamReactions(self):
        rxn_left = 0
        rxn_right = 0
        for load in self.PLs:
            rxn_left, rxn_right += load.getReactionsFromSinglePointLoad()

        return rxn_left, rxn_right

class PointLoad:
    def __init__(self, beam, color, magnitude, location):
        self.startLocation = location
        self.magnitude = magnitude
        self.color = color
        self.beam = beam
        self.type = 'point'

        # # if x is greater then L minus right cantilever, it's on the right cantilever
        # if self.x > self.beam.L-self.beam.Rcant) pass

        # # if x less than len(left cantilever), it's on the left cantilever
        # else if self.x < self.beam.Lcant)
        #     pass

        # # else the load is between the supports
        # else pass

        self.a = self.x - self.beam.Lcant    
        self.b = self.beam.L_btwn_supports - self.a
        self.rxn_left = (self.p * self.b) / (self.beam.L) # untested
        self.rxn_right = (self.p * self.a) / (self.beam.L) # untested

        # self.beam.addPointLoad(self)

    def getReactionsFromSinglePointLoad(self):
        self.a = self.startLocation - self.beam.Lcant
        self.b = self.beam.L_btwn_supports - self.a

        return (self.magnitude * self.b) / (self.beam.L), self.magnitude * self.a / (self.beam.L)


class Dist:
    def __init__(self,color, magnitude, startLocation, endLocation, endMagnitude=None):
        self.color = color
        self.magnitude = magnitude
        self.startLocation = startLocation
        self.endLocation = endLocation
        self.endMagnitude = endMagnitude

# this class was copied from 
class FrameMember(sc.Member):
	
	nDoFPerNode = 3
	
	@property
	def k(self):
		"""Local member stiffness matrix"""
		L = self.length
		E = self.material.E
		A = self.cross.A
		I = self.cross.Ix

		a = (A*E)/L
		b = (E*I)/L
		c = (E*I)/L**2
		d = (E*I)/L**3
		
		return np.array([
			[ a,  0,     0,    -a, 0,     0    ],
			[ 0,  12*d,  6*c,  0,  -12*d, 6*c  ],
			[ 0,  6*c,   4*b,  0,  -6*c,  2*b  ],
			[ -a, 0,     0,    a,  0,     0    ],
			[ 0,  -12*d, -6*c, 0,  12*d,  -6*c ],
			[ 0,  6*c,   2*b,  0,  -6*c,   4*b ]
		])

	@property
	def T(self):
		"""Local to global transformation matrix"""
		l = self.unVec[0]
		m = self.unVec[1]

		return np.array([
			[l,  m, 0, 0,  0, 0],
			[-m, l, 0, 0,  0, 0],
			[0,  0, 1, 0,  0, 0],
			[0,  0, 0, l,  m, 0],
			[0,  0, 0, -m, l, 0],
			[0,  0, 0, 0,  0, 1]
		])