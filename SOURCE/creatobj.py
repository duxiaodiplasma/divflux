import numpy as np
class fida(object):
    """A car for sale by Jeffco Car Dealership.

    Attributes:
        sold_on: The date the vehicle was sold.
    """

    def __init__(self,shot,ch,wavelength,tr,comment):
        """Return a new Car object."""
        self.shot = shot
        self.ch = ch
        self.wavelength = wavelength
        self.tr = tr
        self.comment = comment


class div(object):

    def __init__(self,shot,radius,S,Tau,t,data):

        S = np.piecewise(t,[(t<=np.mean(t)), (t>np.mean(t))],[S,-S])
        self.S = S
        self.shot = shot
        self.radius = radius
        self.Tau = Tau
        self.time=t
        self.data=data



