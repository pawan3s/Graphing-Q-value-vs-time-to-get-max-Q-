import numpy as np
from math import log
import matplotlib.pyplot as plt


# Equations
def density(height: float) -> float:
    """
    Returns the air density in slug/ft^3 based on altitude
    Equations from https://www.grc.nasa.gov/www/k-12/rocket/atmos.html
    :param height: Altitude in feet
    :return: Density in slugs/ft^3
    """
    if height < 36152.0:
        temp = 59 - 0.00356 * height
        p = 2116 * ((temp + 459.7)/518.6)**5.256
    elif 36152 <= height < 82345:
        temp = -70
        p = 473.1*np.exp(1.73 - 0.000048*height)
    else:
        temp = -205.05 + 0.00164 * height
        p = 51.97*((temp + 459.7)/389.98)**-11.388

    rho = p/(1718*(temp+459.7))
    return rho
#inputs
#source: https://en.wikipedia.org/wiki/Unha
m0 = 5944 #slugs
T = 26800 #slugsft/s^2
mass_rate = 3.3 #slugs/sec
eject_vel = 8121 #ft/s

def velocity(time: float) -> float:
    """
    Convert time to velocity using V = V*ln(mi/mf)
    (where mi= Initial mass of rocket,
    mf = instantaneous mas as fuel gets burnt
    :param time: int time in seconds
    :return: velocity in m/s
    """
    return eject_vel*log(m0/(m0-mass_rate*time))


def altitude(time: float) -> float:
    """
    Convert time to altitude using the eqn for rocket
    x = V*[t + (mi/b -t)* ln(1-bt/mi)] where V is ejection velocity
    mi = initial mass, b = fuel consumption rate
    :param time: Time in seconds
    :return: Altitude in m
    """
    f1 = (m0/mass_rate) -time
    f2 = log(1-(mass_rate*time/m0))
    return eject_vel*(time + f1*f2)

if __name__ == '__main__':
    plt.style.use('bmh')
    y_values = []
    x_values = np.arange(0.0, 400.0, 0.5)
    for elapsed_time in x_values:
        alt = altitude(elapsed_time)
        # Dynamic pressure q = 0.5*rho*V^2 = 0.5*density*velocity^2
        q = 0.5 * density(alt) * velocity(elapsed_time) ** 2
        y_values.append(q)

    plt.plot(x_values, y_values, 'b-'
             )
    max_val = max(y_values)
    ind = y_values.index(max_val)

    # Plot an arrow and text with the max value
    plt.annotate('{:.0f} psf @ {} s'.format(max_val, x_values[ind]),
                 xy=(x_values[ind] + 2, max_val),
                 xytext=(x_values[ind] + 15, max_val + 15),
                 arrowprops=dict(facecolor='red', shrink=0.05),
                 )
    # plot the point of Max Q
    plt.plot(x_values[ind], max_val, 'rx')

    plt.xlim(0, 400)
    plt.xlabel('Time (s)')
    plt.ylabel('Pressure (psf)')
    plt.title('Dynamic pressure as a function of time')
    plt.legend()
    plt.show()
