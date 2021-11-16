from django.db import models

class BeamProperties(models.Model):
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
    L = models.DecimalField(max_digits=8, decimal_places=4)
    E = models.DecimalField(max_digits=10, decimal_places=4)
    I = models.DecimalField(max_digits=10, decimal_places=4)
    A = models.DecimalField(max_digits=10, decimal_places=4)
    Lcant = models.DecimalField(max_digits=8, decimal_places=4)
    Rcant = models.DecimalField(max_digits=8, decimal_places=4)

    @property
    def L_btwn_supports(self):
        return self.L - self.Lcant - self.Rcant

    # left_support_restraints = left_support_type
    # left_support_type = right_support_type
    # PLs = []
    # DLs = []
    # POIs = []
    # maxPL = 0
    # maxDL = 0 


    # def defineLoad(self, color, magnitude, startLocation, endLocation=None, endMagnitude=None):
    #     # determine if point or dist load
    #     if endLocation:
    #         load = Dist(color, magnitude, startLocation, endLocation)
    #         self.DLs.push(load)
    #         load.index = self.DLs.length-1
    #         load.type = 'dist'

    #         if math.abs(load.magnitude) > self.maxDL:
    #             self.maxDL = math.abs(load.magnitude)
    #             load.isMaxDL = True

    #             for item in self.DLs:
    #                 item.isMaxDL = False

    #         else:
    #             load.isMaxDL = False
        
    #     else:
    #         load = Point(color, magnitude, startLocation)
    #         self.PLs.push(load)
    #         load.index = self.PLs.length-1
    #         load.type = 'point'

    #         if math.abs(load.magnitude) > self.maxPL:
    #             self.maxPL = math.abs(load.magnitude)
    #             load.isMaxPL = True

    #             for item in self.PLs:
    #                 item.isMaxPL = False

    #         else:
    #             load.isMaxPL = False
    
    @property
    def getBeamReactions(self):
        rxn_left = 0
        rxn_right = 0
        for load in self.PLs:
            load_rxn_left, load_rxn_right = load.getReactionsFromSinglePointLoad()
            rxn_left += load_rxn_left
            rxn_right += load_rxn_right

        return rxn_left, rxn_right

class loadCase(models.Model):
    case_name = models.CharField(max_length=10)

    # # definitely remove null and blank in the future to make the employer required
    # employer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.case_name}'
class pointLoad(models.Model):
    index = models.IntegerField()
    # definitely remove null and blank in the future to make the load case required
    load_case = models.ForeignKey(loadCase, on_delete=models.CASCADE, null=True, blank=True)
    # beam = models.ForeignKey(BeamProperties, on_delete=models.CASCADE, null=True, blank=True)
    magnitude = models.DecimalField(max_digits=8, decimal_places=2)
    location = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.load_case} {self.magnitude} {self.location}'


    def getReactionsFromSinglePointLoad(self):
        self.a = self.location - self.beam.Lcant
        self.b = self.beam.L_btwn_supports - self.a

        return (self.magnitude * self.b) / (self.beam.L), self.magnitude * self.a / (self.beam.L)