"""
    This code fits 2 gaussian components on the observed data, 
    using the PYMC algorithm. 

                            Marcus - 07/05/2018
"""

import numpy as np
import pymc
import matplotlib.pyplot as plt

def gauss_fit(mu, sigma, A, x):
    """
     gaussian function
    """
    return A * np.exp(-((mu - x)**2) / (2. * sigma**2))

def model(x, f): 
    """
     PYMC model to fit 2 gaussian component 
    """
 

    # Priors are uniform...

    sigma1 = pymc.Uniform('sigma1', 0.01, 5.0, value=1.0)
    mu1 = pymc.Uniform('mu1', -1.0, 1.0, value= 0.0)
    A1 = pymc.Uniform('A1', 0.0, 5.0, value= 1.0)

    sigma2 = pymc.Uniform('sigma2', 0.01, 5.0, value=1.0)
    mu2 = pymc.Uniform('mu2', -1.0, 1.0, value= 0.0)
    A2 = pymc.Uniform('A2', 0.0, 5.0, value= 1.0)

    # Model (gauss)

    @pymc.deterministic(plot=False)
    def gauss(x = x, mu1 = mu1,mu2 = mu2, sigma1 = sigma1, sigma2 = sigma2, A1 = A1, A2 = A2):
        return gauss_fit(mu1, sigma1, A1, x) + gauss_fit(mu2, sigma2, A2, x)

    # Weights = 1/ error**2

    y = pymc.Normal('y', mu = gauss, tau = (1.0 / error**2), value = f, observed=True)

    return locals()

np.random.seed(76523654)

############################################################

if __name__ == "__main__":

    # INPUT parameters of the gaussian function

    mu1_initial = 0.
    sigma1_initial = 0.5
    A1_initial = 3.

    mu2_initial = 0.
    sigma2_initial = 5.
    A2_initial = 1.

    print 'Initial Values:'
    print 'Gauss1:', mu1_initial, sigma1_initial, A1_initial
    print 'Gauss2:', mu2_initial, sigma2_initial, A2_initial

    # Array of the INITIAL fake data

    x0 = np.arange(-5., 5., 0.1)
    f0 = gauss_fit(mu1_initial, sigma1_initial, A1_initial, x0) + \
    gauss_fit(mu2_initial, sigma2_initial, A2_initial, x0) 

    # Add some perturbation to the data 
    error = np.ones(len(f0)) # uniform error 
    # Perturb the initial array     
    f_error = f0 + error * np.random.normal(0., 1., len(f0)) * 0.2                                

    # Run PYMC...

    MDL = pymc.MCMC(model(x0, f_error))
    MDL.sample(2e4)

    print 'Fitted parameters (2sigma c.l.s):'
    print 
    print 'mu1=', MDL.mu1.stats()['quantiles'][2.5], MDL.mu1.stats()['mean'], MDL.mu1.stats()['quantiles'][97.5]
    print 'mu2=', MDL.mu2.stats()['quantiles'][2.5], MDL.mu2.stats()['mean'], MDL.mu2.stats()['quantiles'][97.5]
    print 'sigma1=', MDL.sigma1.stats()['quantiles'][2.5], MDL.sigma1.stats()['mean'], MDL.sigma1.stats()['quantiles'][97.5]
    print 'sigma2=', MDL.sigma2.stats()['quantiles'][2.5], MDL.sigma2.stats()['mean'], MDL.sigma2.stats()['quantiles'][97.5]
    print 'A1=', MDL.A1.stats()['quantiles'][2.5], MDL.A1.stats()['mean'], MDL.A1.stats()['quantiles'][97.5]
    print 'A2=', MDL.A2.stats()['quantiles'][2.5], MDL.A2.stats()['mean'], MDL.A2.stats()['quantiles'][97.5]

    # Plotting the fitted data

    y_fit = MDL.stats()['gauss']['mean']
    y_1 = MDL.stats()['gauss']['quantiles'][2.5]
    y_2 = MDL.stats()['gauss']['quantiles'][97.5]
    plt.plot(x0, f_error)
    plt.plot(x0, y_fit, lw = 1., color = 'black')
    plt.fill_between(x0, y_2, y_1, color = 'green', alpha = 0.3)
    plt.xlabel('x')
    plt.ylabel('N')
    plt.show()

    exit()