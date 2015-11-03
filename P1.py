from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def inicializa_T(T, N_steps, dx):
    '''
    Rellena T con las condiciones iniciales del problema.
    Se asegura que las condiciones en los bordes sean cero.
    '''
    for i in range(N_steps):
        x = i * dx
        T[i] = np.exp((-x**2)/0.1)
    T[0] = 1
    T[-1] = 0


def calcula_b(b, N_steps, r):
    for j in range(1, N_steps - 1):
        b[j] = r * T[j+1] + ((1-2*r) + dt * mu * (1-T[j])) * T[j] + r * T[j-1]


def calcula_alpha_y_beta(alpha, beta, b, r, N_steps):
    Aplus = -1 * r
    Acero = (1 + 2 * r)
    Aminus = -1 * r
    alpha[0] = 0
    beta[0] = 1
    for i in range(1, N_steps):
        alpha[i] = -Aplus / (Acero + Aminus*alpha[i-1])
        beta[i] = (b[i] - Aminus*beta[i-1]) / (Aminus*alpha[i-1] + Acero)


def avanza_paso_temporal(T, T_next, alpha, beta, N_steps):

    T_next[0] = 1
    T_next[-1] = 0
    for i in range(N_steps - 2, 0, -1):
        T_next[i] = alpha[i] * T_next[i+1] + beta[i]

def mostar_resultado(sol):

    fig, ax = plt.subplots()
    x_values = np.linspace(x_ini, x_fin, dis_x)
    ax.set_ylim(0, 1)
    ax.set_xlim(0, 1)
    ax.set_xlabel("X")
    ax.set_ylabel("Densidad")
    ax.set_title("Densidad en el espacio para tiempo entre t=0 y t=10")

    for i in range(0, dis_t):
        ax.plot(x_values, sol[i, :], color="r")
    fig.savefig("plot1.jpg")
    # animacion
    fig2, ax2 = plt.subplots()
    ims = []
    ax2.set_xlabel("X en unidades arbitrarias de espacio")
    ax2.set_ylabel("Densidad en unidades arbitrarias")
    ax2.set_title("Densidad en el espacio para tiempo entre t=0 y t=10")
    for add in np.arange(dis_t):
        ims.append(plt.plot(x_values, sol[add, :], color="b", label="t= " + str(add)))
    im_ani = animation.ArtistAnimation(fig2, ims, interval=50, repeat_delay=3000,
                                       blit=True)
    plt.show()

# Main

# setup
t_ini = 0
t_fin = 10
x_ini = 0
x_fin = 1

dis_t = 100
dis_x = 500

dt = (t_fin - t_ini) / (dis_t - 1)
dx = (x_fin - x_ini) / (dis_x - 1)

gamma = 0.001
r = (gamma * dt) / (2 * dx**2)

mu = 1.5

T = np.zeros(dis_x)
T_next = np.zeros(dis_x)

b = np.zeros(dis_x)
alpha = np.zeros(dis_x)
beta = np.zeros(dis_x)

inicializa_T(T, dis_x, dx)


# Queremos guardar las soluciones en cada paso
T_solucion = np.zeros((dis_t, dis_x))
T_solucion[0, :] = T.copy()

for i in range(1, dis_t):
    calcula_b(b, dis_x, r)
    calcula_alpha_y_beta(alpha, beta, b, r, dis_x)
    avanza_paso_temporal(T, T_next, alpha, beta, dis_x)
    T = T_next.copy()
    T_solucion[i, :] = T.copy()

mostar_resultado(T_solucion)