import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button, Slider
import random
from matplotlib.widgets import CheckButtons
import statistics
from scipy.signal import filtfilt, butter
"""
алу з шумом та відфільтрований графік,
а якщо змінити значення на зелених слайдерах, зміниться графік сигналу без шумів.
Справа знизу є меню, де Ви можете вибрати, який з графіків відобразити.
"""
#Задамо значенння констант та функцій, які будемо використовувати
t = np.arange(0.0, 1.0, 0.001)
w = np.arange(0.0, 1.0, 0.001)
a = 2
a1 = 2.5
f =  np.arange(0.0, 1.0, 0.001)
s = a*np.sin(w*t+f)
t1 = np.arange(0.0, 1.0, 0.001)
gaussian_noise = np.random.normal(0, 0.5, 1000)
p = a1*np.sin(w*t1+f)+gaussian_noise
var = statistics.variance(p)
s1 = a1*np.sin(w*t1+f)+gaussian_noise*var
x, y = butter(3, 0.05)
s2 = filtfilt(x, y, s1)
#Зобразимо графіки  функцій
fig, ax = plt.subplots()
l0, = ax.plot(t, s, lw=2, color='k', label='Гармонічні коливання')
l1, = ax.plot(t, s1, lw=2, color='r', label='З шумом')
l2, = ax.plot(t, s2, lw=2, color='b', label='Відфільтрований сигнал')
plt.subplots_adjust(bottom=0.4)

#Визначимо місце, де згаходитимуться слайдери. 
ax_freq = fig.add_axes([0.25, 0.1, 0.65, 0.03])
ax_amp = fig.add_axes([0.25, 0.15, 0.65, 0.03])
ax_phase = fig.add_axes([0.25, 0.2, 0.65, 0.03])
ax_noise_mean = fig.add_axes([0.25, 0.25, 0.65, 0.03])
ax_noise_var = fig.add_axes([0.25, 0.3, 0.65, 0.03])
allowed_amplitudes = np.concatenate([np.linspace(.1, 5, 100), [6, 7, 8, 9]])

#Створимо слайдери
samp = Slider(
    ax_amp, "Harmonic amplitude", 0.1, 9.0,
    valinit=a, valstep=allowed_amplitudes,
    color="green"
)

sfreq = Slider(
    ax_freq, "Harmonic frequensy", 0, 10*np.pi,
    valinit=2*np.pi, valstep=np.pi,
    initcolor='none',
    color="green"
)
sphase = Slider(
    ax_phase, "Harmonic phase", 0, 2*np.pi,
    valinit=np.pi, valstep=0.03*np.pi,
    initcolor='none',
    color="green"
)
snoiseamp = Slider(
    ax_noise_mean, "Noise amplitude", 0.1, 9.0,
    valinit=a1, valstep=allowed_amplitudes,
    initcolor='none'
)
snoisevar = Slider(
    ax_noise_var, "Noise varience", 1, 9.0,
    valinit=var, valstep=0.004,
    initcolor='none'
)
#Визначимо, коли дані будуть оновлюватись та як відображатимуться
def update(val):
    amp = samp.val
    freq = sfreq.val
    phase = sphase.val
    noise = snoiseamp.val
    varience = snoisevar.val
    l0.set_ydata(amp*np.sin(freq*t+phase))
    l1.set_ydata(amp*noise*np.sin(freq*t+phase)+gaussian_noise*varience)
    l2.set_ydata(filtfilt(x, y, (amp*noise*np.sin(freq*t+phase)+gaussian_noise*varience)))
    fig.canvas.draw_idle()

#Оновимо значення
sfreq.on_changed(update)
samp.on_changed(update)
sphase.on_changed(update)
snoiseamp.on_changed(update)
snoisevar.on_changed(update)
#Створимо кнопку, щоб скинути внесені зміни
ax_reset = fig.add_axes([0.8, 0.025, 0.1, 0.04])
button = Button(ax_reset, 'Reset', hovercolor='0.975')
#Створимо функцію для скидання змін
def reset(event):
    sfreq.reset()
    samp.reset()
    sphase.reset()
    snoiseamp.reset()
button.on_clicked(reset)
#Створимо функцію для того, щоб відображати або не відображати графіки в зележності
#від опції, вибраної в меню.
lines = [l0, l1, l2]
labels = ["Без шуму", "З шумом", 'Відфільтрований сигнал']
def func(label):
    index = labels.index(label)
    lines[index].set_visible(not lines[index].get_visible())
    fig.canvas.draw() 
label = [True, True, True]
#Створимо кнопку меню для попередньої функції. 
ax_check = plt.axes([0.9, 0.001, 0.2, 0.3])
plot_button = CheckButtons(ax_check, labels, label)
plot_button.on_clicked(func)
 
plt.show()
