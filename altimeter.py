import os
from machine import Pin, I2C, ADC
import time
import bmp280

# Configuração I2C para sensor BMP280
i2c = I2C(scl=Pin(22), sda=Pin(21))
bmp = bmp280.BMP280(i2c)

# Configuração de pinos para medição de tensão da bateria
battery_voltage = ADC(Pin(35))

# Configuração de pinos para ejeção de paraquedas
parachute_eject = Pin(15, Pin.OUT)

# Altitude na qual definir o apogeu
apogee_altitude = 100 # em metros

# Queda mínima de altitude para acionar a ejeção do paraquedas
min_drop = 2 # em metros

# Tensão mínima da bateria necessária para implantação
min_voltage = 3.6 # em volts

# Abrir o arquivo para gravar dados de altitude
f = open('altitude_data.txt', 'w')

# Loop para monitorar continuamente a altitude e a tensão da bateria
while True:
  # Ler a altitude do sensor BMP280
  current_altitude = bmp.altitude
  
  # Ler a voltagem da bateria
  battery_level = battery_voltage.read() * (3.3 / 4096)
  
  if current_altitude <= apogee_altitude + min_drop and battery_level >= min_voltage:
    # Ejetar paraquedas
    parachute_eject.value(1)
    
    # Aguarde o paraquedas abrir totalmente
    time.sleep(5)
    
    # Desligue a ejeção do paraquedas
    parachute_eject.value(0)
    
    # Sair do loop
    break
  
  # Escreva a altitude atual no arquivo
  f.write(str(current_altitude) + '\n')
  
  # Aguarde as próximas leituras de altitude e tensão da bateria
  time.sleep(0.5)

# Feche o arquivo após a conclusão da coleta de dados
f.close()
