import numpy as np
import pymc
import matplotlib.pyplot as plt

def model(x, f): 

    # Priors are uniform...

    sigma = pymc.Uniform('sigma', 0.01, 5.0, value=1.0)
    mu = pymc.Uniform('mu', -1.0, 1.0, value= 0.0)
    A = pymc.Uniform('A', 0.0, 5.0, value= 1.0)

    # Model (gauss)

    @pymc.deterministic(plot=False)
    def gauss(x = x, mu = mu, sigma= sigma, A = A):
        return A * np.exp(-((mu - x)**2) / (2. * sigma**2))

    # Weights = 1/ error**2

    y = pymc.Normal('y', mu = gauss, tau = (1.0 / error**2), value = f, observed=True)

    return locals()

np.random.seed(76523654)

############################################################

if __name__ == "__main__":

    # INPUT parameters of the gaussian function

    mu0 = 0.
    sigma0 = 1.
    A0 = 3.
    print 'initial values:', mu0, sigma0, A0

    # Array of the INITIAL fake data

    x0 = np.arange(-5., 5., 0.1)
    f0 = A0 * np.exp(-((mu0 - x0)**2) / (2. * sigma0**2))

    # Add some perturbation to the data 
    error = np.ones(len(f0)) # uniform error 
    # Perturb the initial array     
    f_error = f0 + error * np.random.normal(0., 1., len(f0)) * 0.2                                

    # Run PYMC...

    MDL = pymc.MCMC(model(x0, f_error))
    MDL.sample(2e4)

    print 'Fitted parameters (2sigma c.l.s):'
    print 
    print 'mu=', MDL.mu.stats()['quantiles'][2.5], MDL.mu.stats()['mean'], MDL.mu.stats()['quantiles'][97.5]
    print 'sigma=', MDL.sigma.stats()['quantiles'][2.5], MDL.sigma.stats()['mean'], MDL.sigma.stats()['quantiles'][97.5]
    print 'A=', MDL.A.stats()['quantiles'][2.5], MDL.A.stats()['mean'], MDL.A.stats()['quantiles'][97.5]

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