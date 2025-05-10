import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox

temperature = ctrl.Antecedent(np.arange(0, 41, 1), 'sıcaklık')
fan_speed = ctrl.Consequent(np.arange(0, 101, 1), 'fan_hızı')

temperature['soğuk'] = fuzz.trapmf(temperature.universe, [0, 0, 10, 20])
temperature['ılık'] = fuzz.trimf(temperature.universe, [10, 20, 30])
temperature['sıcak'] = fuzz.trapmf(temperature.universe, [20, 30, 40, 40])

fan_speed['yavaş_hız'] = fuzz.trimf(fan_speed.universe, [0, 0, 50])
fan_speed['orta_hız'] = fuzz.trimf(fan_speed.universe, [0, 50, 100])
fan_speed['yüksek_hız'] = fuzz.trimf(fan_speed.universe, [50, 100, 100])

rule1 = ctrl.Rule(temperature['soğuk'], fan_speed['yavaş_hız'])
rule2 = ctrl.Rule(temperature['ılık'], fan_speed['orta_hız'])
rule3 = ctrl.Rule(temperature['sıcak'], fan_speed['yüksek_hız'])

fan_speed_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
fan_speed_simulator = ctrl.ControlSystemSimulation(fan_speed_ctrl)

def fan_hizi_hesapla():
    try:
        sicaklik = float(entry_sicaklik.get())

        if sicaklik < 0 or sicaklik > 40:
            messagebox.showerror("Hata", "Lütfen sıcaklık değerini 0 ile 40 arasında girin.")
            return
        fan_speed_simulator.input['sıcaklık'] = sicaklik
        fan_speed_simulator.compute()

        fan_hizi = fan_speed_simulator.output['fan_hızı']
        label_sonuc.config(text=f"Fan Hızı: {fan_hizi:.2f} %")

    except ValueError:
        messagebox.showerror("Hata", "Lütfen geçerli bir sayı girin.")


def grafik_sicaklik():
    temperature.view()
    plt.show()


def grafik_fan_hizi():
    fan_speed.view()
    plt.show()


root = tk.Tk()
root.title("Bulanık Mantık Fan Kontrolü")

label_sicaklik = tk.Label(root, text="Sıcaklık (°C):")
label_sicaklik.pack(pady=10)

entry_sicaklik = tk.Entry(root)
entry_sicaklik.pack(pady=10)

label_sonuc = tk.Label(root, text="Fan Hızı: 0 %")
label_sonuc.pack(pady=20)

button_hesapla = tk.Button(root, text="Fan Hızını Hesapla", command=fan_hizi_hesapla)
button_hesapla.pack(pady=20)

button_sicaklik_grafik = tk.Button(root, text="Sıcaklık Grafiğini Göster", command=grafik_sicaklik)
button_sicaklik_grafik.pack(pady=10)
button_fan_hizi_grafik = tk.Button(root, text="Fan Hızı Grafiğini Göster", command=grafik_fan_hizi)
button_fan_hizi_grafik.pack(pady=10)

root.mainloop()
