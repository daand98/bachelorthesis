import matplotlib.pyplot as plt
import numpy as np
import math

# Dictionary of dictionaries with the data (bright stars all in one fit) inside
dict = {'290347-2006':{'type':'Swift J174553.7-290347',     'color':'green', 'gamma':1.7502, 'gamma+':0.3474, 'gamma-':0.3273, 'flux':-11.2593, 'flux+':0.1425, 'flux-':0.1042},
        '290005-2006':{'type':'CXOGC J174540.0-290005',     'color':'lime',  'gamma':2.3799, 'gamma+':0.3908, 'gamma-':0.3650, 'flux':-10.3148, 'flux+':0.2325, 'flux-':0.1780},
        '290124-2006':{'type':'CXOGC J174535.5-290124',     'color':'purple','gamma':0.3436, 'gamma+':0.5200, 'gamma-':0.5326, 'flux':-11.9944, 'flux+':0.0515, 'flux-':0.0541},
        '290634-2006':{'type':'Swift J174622.1-290634',     'color':'gray',  'gamma':2.7719, 'gamma+':0.7594, 'gamma-':0.7279, 'flux':-10.9828, 'flux+':0.4683, 'flux-':0.3327},
        '290124-2008':{'type':'CXOGC J174535.5-290124',     'color':'purple','gamma':0.7612, 'gamma+':0.7313, 'gamma-':0.7128, 'flux':-11.9072, 'flux+':0.0977, 'flux-':0.0843},
        '290022-2009':{'type':'CXOGC J174538.0-290022',     'color':'black', 'gamma':1.2731, 'gamma+':0.4681, 'gamma-':0.4547, 'flux':-10.8934, 'flux+':0.1132, 'flux-':0.0772},
        '285921-2011':{'type':'Swift J174535.5-285921',     'color':'orange','gamma':2.2734, 'gamma+':1.0734, 'gamma-':0.9949, 'flux':-10.7822, 'flux+':0.5611, 'flux-':0.2743},
        '285921-2016':{'type':'Swift J174535.5-285921',     'color':'orange','gamma':1.7460, 'gamma+':0.4022, 'gamma-':0.3837, 'flux':-10.7593, 'flux+':0.1590, 'flux-':0.1145},
        '290005-2017':{'type':'CXOGC J174540.0-290005',     'color':'lime',  'gamma':2.2127, 'gamma+':0.4582, 'gamma-':0.4350, 'flux':-10.5665, 'flux+':0.2344, 'flux-':0.1677},
        '285921-2020':{'type':'Swift J174535.5-285921',     'color':'orange','gamma':1.4265, 'gamma+':0.4244, 'gamma-':0.4077, 'flux':-10.9259, 'flux+':0.1235, 'flux-':0.0862}
}

# Turns the flux from the fit (in erg/s/cm^2) into a luminosity (in erg/s).
def flux(data, distance):

    # Conversion factor of luminosity from the distance to here (4*pi*(distance in cm)^2)
    constant = 4 * math.pi * (distance * (3.0857 * 10**18)) ** 2
    
    # Calculates the values of the luminosity and the error for each object
    fitvalue = data['flux']

    data['flux'] = constant * (10 ** data['flux'])
    data['flux+'] = (constant * (10 ** (fitvalue + data['flux+']))) - data['flux']
    data['flux-'] = abs((constant * (10 ** (fitvalue - data['flux-']))) - data['flux'])

    return data

# Main function
def main(objects, distance):

    # If we type 'all' in the functions parameters, it plots all of them.
    if objects == 'all':
        objects = dict.keys()
    
    objectlist = []

    # Loops through all objects we want and plots the results with correct errors.
    for object in objects:

        data = flux(dict[str(object)], distance)

        y = data['gamma']
        ymin = data['gamma-']
        ymax = data['gamma+']

        x = data['flux']
        xmin = data['flux-']
        xmax = data['flux+']

        if data['type'] in objectlist:
            plt.errorbar(x, y, xerr=np.array([[xmin, xmax]]).T, yerr=np.array([[ymin, ymax]]).T, fmt='o', color=data['color'], capsize=2, markersize=5)

        else:
            plt.errorbar(x, y, xerr=np.array([[xmin, xmax]]).T, yerr=np.array([[ymin, ymax]]).T, label=data['type'], fmt='o', color=data['color'], capsize=2, markersize=5)
            objectlist.append(data['type'])

    # Make plot nicer.
    plt.ylabel("Photon index", fontsize=15)
    plt.xlabel('X-ray luminosity (2-10 keV; erg/s)', fontsize=15)
    plt.xscale('log')
    plt.legend(loc='lower right', fontsize=10)
    plt.ylim(-1, 4)
    plt.xlim(5e+33, 1e+36)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.minorticks_on()
    plt.tight_layout()
    plt.savefig("Errorplot.png", dpi=1000)
    plt.show()

main('all', 8000)
