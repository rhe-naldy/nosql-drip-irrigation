This repository serves as an archive for a research paper titled ["Precision Agriculture: Soil Moisture-based IoT Drip Irrigation System to Optimize Water Usage for Aglaonema in Greenhouse Environment"](https://ijhst.ut.ac.ir/article_101039_b627a252ff56bf7ad8794ce35e8b953c.pdf), published in the [International Journal of Horticultural Science and Technology](https://ijhst.ut.ac.ir/). This research was conducted as part of the authors' Bachelor's degree thesis.
  
The paper presents the development of a smart IoT-based irrigation system designed to optimize water usage by testing various soil moisture levels for the plant Aglaonema 'Stardust'. The system collects data from multiple sensors, with a Raspberry Pi 3B board used to send sensor data collected by the three drip irrigation module (Arduino Uno R3) to Microsoft Azure's CosmosDB, while the Arduino Uno R3 microcontrollers handle both irrigation and data collection at the plant level. The study conducts an experiment with four Aglaonema plants of the same species, each exposed to distinct soil moisture levels: Plant A (45-55%), Plant B (55-65%), Plant C (65-75%)—all utilizing a drip irrigation system—and Plant D, which received manual watering. The study also examined supplementary factors such as leaf count, which ranged from 11 to 17 leaves, and pot size, which had a diameter of 17 cm.

In each plant configuration, an Arduino Uno R3 board gathers the environmental data pertaining to the plant. This board is linked to multiple electrical components, such as the HW-390 capacitive soil moisture sensor, DHT22 sensor, GY-302 BH1750 sensor, YFS401 water flow sensor, submersible mini-water pumps, and the IRF520 MOSFET driver module. Meanwhile, the energy required to operate the pump is derived from a 3.7-volt battery.

The firmware for both arduino and raspberry pi board can be accessed in the corresponding folders, namely [arduino/arduino_firmware.ino](https://github.com/rhe-naldy/nosql-drip-irrigation/blob/main/arduino/arduino_firmware.ino) and [raspberry_pi/send_data.py](https://github.com/rhe-naldy/nosql-drip-irrigation/blob/main/raspberry_pi/send_data.py).
  
  
Below are a detailed image of the system architecture and circuit diagram, which can be seen below.
  
* The proposed system architecture diagram
  
<img src="https://github.com/rhe-naldy/nosql-drip-irrigation/blob/main/system_architecture_diagram.png?raw=true" width="512">
  
  
  
* The drip irrigation circuit diagram
  
<img src="https://github.com/rhe-naldy/nosql-drip-irrigation/blob/main/drip_irrigation_circuit_diagram.png?raw=true" width="512">
