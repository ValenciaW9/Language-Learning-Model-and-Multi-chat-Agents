import random
import time
import openai

# Set the OpenAI API key
openai.api_key = ""

# Function to get a response from ChatGPT 4.0 Mini
def get_chatgpt_mini_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use "gpt-4" or another available model
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        return response.choices[0].message['content']
    except Exception as e:
        print(f"Error communicating with OpenAI: {e}")
        return None

# Class to define RISC-V processors with GPU support
class RISCVProcessor:
    def __init__(self, name, clock_speed, cores, power_consumption, gpu):
        self.name = name
        self.clock_speed = clock_speed  # GHz
        self.cores = cores
        self.power_consumption = power_consumption  # Watts
        self.gpu = gpu  # GPU Type

    def display_info(self):
        print(f"Processor: {self.name}")
        print(f"Clock Speed: {self.clock_speed} GHz")
        print(f"Cores: {self.cores}")
        print(f"Power Consumption: {self.power_consumption} Watts")
        print(f"GPU: {self.gpu}")

# Define RISC-V boards with processors and sensors
class RISCBoard:
    def __init__(self, name, processor, sensors):
        self.name = name
        self.processor = processor
        self.sensors = sensors

    def display_info(self):
        print(f"Board: {self.name}")
        self.processor.display_info()
        for sensor in self.sensors:
            print(f"Sensor: {sensor['type']} - Reading: {sensor['value']}")

# Generate sensor data with various sensors
def generate_sensor_data():
    return [
        {"type": "Temperature Sensor", "value": random.uniform(25.0, 80.0)},  # Celsius
        {"type": "Power Sensor", "value": random.uniform(10.0, 60.0)},        # Watts
        {"type": "Pressure Sensor", "value": random.uniform(1.0, 10.0)},      # bar
        {"type": "Light Sensor", "value": random.uniform(100, 1000)},         # lumens
        {"type": "Humidity Sensor", "value": random.uniform(30.0, 90.0)},     # Percentage
        {"type": "Accelerometer", "value": random.uniform(0.0, 9.8)},         # m/s^2
        {"type": "Gyroscope", "value": random.uniform(-180, 180)},            # Degrees/sec
        {"type": "Magnetometer", "value": random.uniform(-50, 50)},           # μT (Microteslas)
        {"type": "Proximity Sensor", "value": random.uniform(0, 10)},         # cm
        {"type": "GPS Sensor", "value": (random.uniform(-90, 90), random.uniform(-180, 180))},  # Lat, Long
        {"type": "Ultrasonic Sensor", "value": random.uniform(0, 400)}        # cm
    ]

# Create processors with GPU
processors = [
    RISCVProcessor("SiFive Freedom E300", 1.6, 1, 1.5, "Mali-400 MP"),
    RISCVProcessor("Hummingbird E200", 2.0, 2, 3.0, "Adreno 330"),
    RISCVProcessor("Shakti C-Class", 3.0, 4, 5.5, "NVIDIA GeForce GTX 1650"),
    RISCVProcessor("BOOM v2", 3.5, 6, 6.0, "AMD Radeon RX 5700"),
    RISCVProcessor("VexRiscv", 1.8, 1, 2.0, "Intel UHD 620"),
    RISCVProcessor("RISC-V High-Performance", 4.0, 8, 8.0, "NVIDIA A100"),
]

# Create RISC-V boards with the new processors and sensors
boards = [
    RISCBoard("Arduino Mega RISC-V", processors[0], generate_sensor_data()),
    RISCBoard("RISC-V Raspberry Pi", processors[1], generate_sensor_data()),
    RISCBoard("ESP32 RISC-V Edition", processors[2], generate_sensor_data()),
    RISCBoard("Custom RISC-V Board 1", processors[3], generate_sensor_data()),
    RISCBoard("Custom RISC-V Board 2", processors[4], generate_sensor_data()),
    RISCBoard("Advanced RISC-V Board", processors[5], generate_sensor_data()),
]

# Display sensor data for each board
def display_boards_info():
    start_time = time.time()  # Start benchmark timer
    for board in boards:
        board.display_info()
        print("-" * 40)
    elapsed_time = time.time() - start_time
    print(f"Benchmark: Displaying board info took {elapsed_time:.4f} seconds")

# Example usage
display_boards_info()

# Generate a ChatGPT response based on a prompt
prompt = "Describe the use of RISC-V processors in embedded systems."
chatgpt_response = get_chatgpt_mini_response(prompt)
if chatgpt_response:
    print(f"ChatGPT Response:\n{chatgpt_response}")