import numpy as np
# from numpy.core.shape_base import vstack

from itm import constants


class LCDM:

    def __init__(self) -> None:
        pass

    def hubble(self, z, params):
        # M, h, omega0_b, omega0_cdm = params
        # M = params[0]
        h = params[1]
        omega0_b = params[2]
        omega0_cdm = params[3]

        H0 = 100. * h
        Omega0_b = omega0_b/h**2
        Omega0_cdm = omega0_cdm/h**2
        Omega0_g = constants.radiation_density(h)
        Omega0_de = 1. - Omega0_g - Omega0_b - Omega0_cdm

        rho_tot = 0

        # radiation:
        rho_tot += Omega0_g*H0**2 * np.power(1.+z, 4.)

        # baryons:
        rho_tot += Omega0_b*H0**2 * np.power(1.+z, 3.)

        # cdm:
        rho_tot += Omega0_cdm*H0**2 * np.power(1+z, 3.)

        # scf:
        rho_tot += Omega0_de*H0**2

        return np.sqrt(rho_tot)

    # def hubble_table(self, params):
    #     self._params = params
    #     z_max = 2.5
    #     z = np.linspace(0, z_max, 100)
    #     h = self.hubble(z)
    #     return np.vstack((z, h))