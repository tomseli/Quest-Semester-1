import numpy as np
import matplotlib.pyplot as plt
import math as m

# spindel
pitch = 0.005 # m/rotatie 

# bekende
a = 45          # acceleratie motor[rot*s^-2] 
s = 0.05/pitch  # gewenste afstand motor [rot]
t = 1           
N = int(1e5)
dt = t/N

t1 = 0.5*(t - (m.sqrt(a*t**2 - 4*s))/(m.sqrt(a)))
t3 = 0.5*((m.sqrt(a*t**2 - 4*s))/(m.sqrt(a))+t)
assert t1 < t/2, "acc too low, t1 is not < t/2"

tijd = np.zeros(N)
snelheid = np.zeros(N)
versnelling = np.zeros(N)
positie = np.zeros(N)
for i in range(0, N):
    tijd[i] = tijd[i-1] + dt
    
    if tijd[i] < t1:
        snelheid[i] = snelheid[i-1] + a * dt
    elif tijd[i] >= t3:
        snelheid[i] = snelheid[i-1] - a * dt
    else:
        snelheid[i] = snelheid[i-1] 

    versnelling[i] = (snelheid[i] - snelheid[i-1])/dt
    positie[i] = positie[i-1] + snelheid[i]*dt

print("Afgelegde afstand:", str(np.sum(snelheid)*dt), "rotaties")

plt.figure(figsize=(6,10))

plt.subplot(3, 1, 1)
plt.plot(tijd, versnelling)
plt.grid()
plt.title("a,t-diagram")
plt.xlabel("Tijd [s]")
plt.ylabel("Versnelling [rot s^-2]")
plt.tight_layout()

plt.subplot(3, 1, 2)
plt.plot(tijd, snelheid)
plt.grid()
plt.title("v,t-diagram")
plt.xlabel("Tijd [s]")
plt.ylabel("Snelheid [rot s^-1]")
plt.tight_layout()

plt.subplot(3, 1, 3)
plt.plot(tijd, positie)
plt.grid()
plt.title("s,t-diagram")
plt.xlabel("Tijd [s]")
plt.ylabel("Positie [rot]")
plt.tight_layout()
plt.show()