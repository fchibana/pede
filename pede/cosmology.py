from abc import ABCMeta, abstractmethod

import numpy as np

from pede import constants
from pede.itm_solver import ITMSolver


class Cosmology(metaclass=ABCMeta):
    @property
    @abstractmethod
    def _name(self):
        pass

    @property
    @abstractmethod
    def _params_names(self):
        pass

    @property
    @abstractmethod
    def _params_initial_guess(self):
        pass

    @abstractmethod
    def get_prior(self, parameters):
        pass

    @abstractmethod
    def rho_cdm(self, x, parameters):
        pass

    @abstractmethod
    def rho_de(self, x, parameters):
        pass

    def get_name(self) -> str:
        return self._name

    def get_params_names(self) -> list:
        return self._params_names

    def get_initial_guess(self) -> list:
        return self._params_initial_guess

    def rho_radiation(self, x, parameters):
        # M = parameters[0]
        h = parameters[1]
        # omega0_b = parameters[2]
        # omega0_cdm = parameters[3]

        H0 = 100.0 * h
        Omega0_g = constants.radiation_density(h)

        Omega0_g = constants.radiation_density(h)
        return Omega0_g * H0**2 * np.power(1.0 + x, 4.0)

    def rho_baryons(self, x, parameters):
        # M = parameters[0]
        h = parameters[1]
        omega0_b = parameters[2]
        # omega0_cdm = parameters[3]

        H0 = 100.0 * h
        Omega0_b = omega0_b / h**2

        return Omega0_b * H0**2 * np.power(1.0 + x, 3.0)

    def hubble(self, x, parameters):
        rho_tot = 0
        rho_tot += self.rho_radiation(x, parameters)
        rho_tot += self.rho_baryons(x, parameters)
        rho_tot += self.rho_cdm(x, parameters)
        rho_tot += self.rho_de(x, parameters)

        return np.sqrt(rho_tot)


class ModelNames:
    LCDM = "lcdm"
    WCDM = "wcdm"
    IDE1 = "ide1"
    IDE2 = "ide2"
    ITM = "itm"


class LCDM(Cosmology):
    _name = ModelNames.LCDM
    _params_names = ["M", "h", "omega_b", "omega_cdm"]
    _params_initial_guess = [25.01, 0.71, 0.025, 0.12]

    def __init__(self) -> None:
        super().__init__()

    def get_prior(self, parameters):
        M = parameters[0]
        h = parameters[1]
        omega0_b = parameters[2]
        omega0_cdm = parameters[3]

        H0 = 100.0 * h
        Omega0_b = omega0_b / h**2
        Omega0_cdm = omega0_cdm / h**2

        p = np.array([M, H0, Omega0_b, Omega0_cdm])

        upper_bound = np.array([30.0, 80.0, 0.10, 0.5])
        lower_bound = np.array([20.0, 60.0, 0.01, 0.1])

        if np.all(p > lower_bound) and np.all(p < upper_bound):
            return 0.0
        else:
            return -np.inf

    def rho_cdm(self, x, parameters):
        # M = parameters[0]
        h = parameters[1]
        # omega0_b = parameters[2]
        omega0_cdm = parameters[3]

        H0 = 100.0 * h
        Omega0_cdm = omega0_cdm / h**2

        return Omega0_cdm * H0**2 * np.power(1 + x, 3.0)

    def rho_de(self, x, parameters):
        # M = parameters[0]
        h = parameters[1]
        omega0_b = parameters[2]
        omega0_cdm = parameters[3]

        H0 = 100.0 * h
        Omega0_b = omega0_b / h**2
        Omega0_cdm = omega0_cdm / h**2
        Omega0_g = constants.radiation_density(h)
        Omega0_de = 1.0 - Omega0_g - Omega0_b - Omega0_cdm

        return Omega0_de * H0**2


class WCDM(Cosmology):
    _name = ModelNames.WCDM
    _params_names = ["M", "h", "omega_b", "omega_cdm", "w"]
    _params_initial_guess = [24.96, 0.69, 0.022, 0.12, -0.99]

    def __init__(self) -> None:
        super().__init__()

    def get_prior(self, parameters):
        M = parameters[0]
        h = parameters[1]
        omega0_b = parameters[2]
        omega0_cdm = parameters[3]
        w = parameters[4]

        H0 = 100.0 * h
        Omega0_b = omega0_b / h**2
        Omega0_cdm = omega0_cdm / h**2

        p = np.array([M, H0, Omega0_b, Omega0_cdm, w])

        upper_bound = np.array([30.0, 80.0, 0.10, 0.5, -0.5])
        lower_bound = np.array([20.0, 60.0, 0.01, 0.1, -1.5])

        if np.all(p > lower_bound) and np.all(p < upper_bound):
            return 0.0
        else:
            return -np.inf

    def rho_cdm(self, x, parameters):
        # M = parameters[0]
        h = parameters[1]
        # omega0_b = parameters[2]
        omega0_cdm = parameters[3]
        # w = parameters[4]

        H0 = 100.0 * h
        # Omega0_b = omega0_b/h**2
        Omega0_cdm = omega0_cdm / h**2
        # Omega0_g = constants.radiation_density(h)
        # Omega0_de = 1. - Omega0_g - Omega0_b - Omega0_cdm

        return Omega0_cdm * H0**2 * np.power(1.0 + x, 3.0)

    def rho_de(self, x, parameters):
        # M = parameters[0]
        h = parameters[1]
        omega0_b = parameters[2]
        omega0_cdm = parameters[3]
        w = parameters[4]

        H0 = 100.0 * h
        Omega0_b = omega0_b / h**2
        Omega0_cdm = omega0_cdm / h**2
        Omega0_g = constants.radiation_density(h)
        Omega0_de = 1.0 - Omega0_g - Omega0_b - Omega0_cdm

        return Omega0_de * H0**2 * np.power(1.0 + x, 3.0 * (1.0 + w))


class IDE1(Cosmology):
    _name = ModelNames.IDE1
    _params_names = ["M", "h", "omega_b", "omega_cdm", "w", "beta"]
    _params_initial_guess = [24.96, 0.69, 0.022, 0.12, -0.99, 0.0]

    def __init__(self) -> None:
        super().__init__()

    def get_prior(self, parameters):
        # M, h, omega0_b, omega0_cdm, w, beta = parameters

        # if w + beta = 0, rho_cdm diverges (1 / 0)
        if abs(parameters[4] + parameters[5]) < 0.001:
            return -np.inf

        upper_bound = np.array([26.0, 0.8, 0.03, 0.3, -0.7, 1])
        lower_bound = np.array([24.0, 0.55, 0.01, 0.01, -1.3, -1])

        if np.all(parameters > lower_bound) and np.all(parameters < upper_bound):
            return 0.0
        else:
            return -np.inf

    def rho_cdm(self, x, parameters):
        # M = parameters[0]
        h = parameters[1]
        omega0_b = parameters[2]
        omega0_cdm = parameters[3]
        w = parameters[4]
        beta = parameters[5]

        H0 = 100.0 * h
        Omega0_b = omega0_b / h**2
        Omega0_cdm = omega0_cdm / h**2
        Omega0_g = constants.radiation_density(h)
        Omega0_de = 1.0 - Omega0_g - Omega0_b - Omega0_cdm

        cdm_factor = Omega0_cdm * H0**2
        coup_factor = (beta / (beta + w)) * Omega0_de * H0**2

        cdm_evol = np.power(1.0 + x, 3.0)
        coup_evol = np.power(1.0 + x, 3.0 * (1.0 + w + beta))

        rho_bare = cdm_factor * cdm_evol
        rho_coup = coup_factor * (cdm_evol - coup_evol)

        return rho_bare + rho_coup

    def rho_de(self, x, parameters):
        # M = parameters[0]
        h = parameters[1]
        omega0_b = parameters[2]
        omega0_cdm = parameters[3]
        w = parameters[4]
        beta = parameters[5]

        H0 = 100.0 * h
        Omega0_b = omega0_b / h**2
        Omega0_cdm = omega0_cdm / h**2
        Omega0_g = constants.radiation_density(h)
        Omega0_de = 1.0 - Omega0_g - Omega0_b - Omega0_cdm

        return Omega0_de * H0**2 * np.power(1.0 + x, 3.0 * (1.0 + w + beta))


class IDE2(Cosmology):
    _name = ModelNames.IDE2
    _params_names = ["M", "h", "omega_b", "omega_cdm", "w", "beta"]
    _params_initial_guess = [24.96, 0.69, 0.022, 0.12, -0.99, 0.0]

    def __init__(self) -> None:
        super().__init__()

    def get_prior(self, parameters):
        # M, h, omega0_b, omega0_cdm, w, beta = parameters

        # if w + beta = 0, rho_de diverges (1 / 0)
        if abs(parameters[4] + parameters[5]) < 0.001:
            return -np.inf

        upper_bound = np.array([26.0, 0.8, 0.03, 0.3, -0.7, 1])
        lower_bound = np.array([24.0, 0.55, 0.01, 0.01, -1.3, -1])

        if np.all(parameters > lower_bound) and np.all(parameters < upper_bound):
            return 0.0
        else:
            return -np.inf

    def rho_cdm(self, x, parameters):
        # M = parameters[0]
        h = parameters[1]
        # omega0_b = parameters[2]
        omega0_cdm = parameters[3]
        # w = parameters[4]
        beta = parameters[5]

        H0 = 100.0 * h
        # Omega0_b = omega0_b/h**2
        Omega0_cdm = omega0_cdm / h**2
        # Omega0_g = constants.radiation_density(h)
        # Omega0_de = 1. - Omega0_g - Omega0_b - Omega0_cdm

        return Omega0_cdm * H0**2 * np.power(1.0 + x, 3.0 * (1.0 - beta))

    def rho_de(self, x, parameters):
        # M = parameters[0]
        h = parameters[1]
        omega0_b = parameters[2]
        omega0_cdm = parameters[3]
        w = parameters[4]
        beta = parameters[5]

        H0 = 100.0 * h
        Omega0_b = omega0_b / h**2
        Omega0_cdm = omega0_cdm / h**2
        Omega0_g = constants.radiation_density(h)
        Omega0_de = 1.0 - Omega0_g - Omega0_b - Omega0_cdm

        de_factor = Omega0_de * H0**2
        coup_factor = (beta / (beta + w)) * Omega0_cdm * H0**2

        de_evol = np.power(1.0 + x, 3.0 * (1.0 + w))
        coup_evol = np.power(1 + x, 3.0 * (1.0 - beta))

        rho_bare = de_factor * de_evol
        rho_coup = coup_factor * (de_evol - coup_evol)

        return rho_bare + rho_coup


# TODO: implement ITM(Cosmology)
class ITM(Cosmology):
    _name = ModelNames.ITM
    _params_names = ["M", "h", "omega_b", "omega_cdm", "w", "beta", "phi0"]
    _params_initial_guess = [24.96, 0.69, 0.022, 0.12, -0.99, 0.0, 0.05]

    def __init__(self) -> None:
        super().__init__()

    def update_and_solve(self, parameters: list) -> None:
        self.itm = ITMSolver(parameters)
        self.itm.solve(z_max=2.0)

    def get_prior(self, parameters):
        # M, h, omega0_b, omega0_cdm, w, beta, phi0 = parameters

        # since dphi0 = sqrt(1 - w0)
        if parameters[4] < -1.0:
            return -np.inf

        upper_bound = np.array([26.0, 0.8, 0.03, 0.3, -0.7, 1.0, 10.0])
        lower_bound = np.array([24.0, 0.55, 0.01, 0.01, -1.0, -1.0, 0.0])

        if np.all(parameters > lower_bound) and np.all(parameters < upper_bound):
            return 0.0
        else:
            return -np.inf

    def rho_cdm(self, x, parameters):
        return self.itm.get_rho_cdm_at_z(x)

    def rho_de(self, x, parameters):
        return self.itm.get_rho_scf_at_z(x)
