
class Beam:
    def __init__(self, L, E, I, A, Lcant, Rcant, left_support_type, right_support_type):
        # This beam class assumes there are only two supports for the beam


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

    def addPointLoad(self, load):
        load.index = len(self.PLs)
        self.PLs.append(load)


        
class PointLoad:
    def __init__(self, p, x, beam):
        # Point Load Class
        # p = magnitude of load
        # x = distance from left end of beam to point load
        # a = distance from left support to point load (negative if the the left)
        # b = distance from right support to point load (negative if the the left)
        # beam = beam object that the load is applied to

        self.p = p
        self.x = x
        self.beam = beam
        self.type = 'point'
        self.error = ''

        # if x is greater then L minus right cantilever, it's on the right cantilever
        if self.x > self.beam.L-self.beam.Rcant:
            pass

        # if x less than len(left cantilever), it's on the left cantilever
        elif self.x < self.beam.Lcant:
            pass

        # else the load is between the supports
        else:
            pass

        self.a = self.x - self.beam.Lcant    
        self.b = self.beam.L_btwn_supports - self.a
        self.rxn_left = (self.p * self.b) / (self.beam.L) # untested
        self.rxn_right = (self.p * self.a) / (self.beam.L) # untested

        beam.addPointLoad(self)

class DistributedLoad:
    def __init__(self, p_start, p_end, l_start, l_end, beam):
        # Dist Load Class
        # p_start = magnitude at start of load
        # p_end = magnitude at end of load
        # l_start = distance from left end of beam to start of distributed load
        # l_end = distance from left end of beam to end of distributed load
        # beam = beam object that the load is applied to

        self.p_start = p_start
        self.p_end = p_end
        self.l_start = l_start
        self.l_end = l_end
        self.beam = beam
        self.type = 'dist'
        self.error = ''


# def shearDiagram(loads):
