# RISC-V Board Simulation with GPT Integration

## Overview

This Python script simulates RISC-V processor-based boards with various sensor data readings, while integrating OpenAI's GPT 4.0 mini model to generate AI responses. The script includes multiple classes, functions, and components to define RISC-V processors, their associated boards, and sensors. Additionally, it provides a feature to interact with the OpenAI GPT model to generate responses based on specific prompts.

## Features

- **RISC-V Processor Class**: Simulates a RISC-V processor with parameters like name, clock speed, cores, power consumption, and GPU type.
- **RISC-V Board Class**: Defines a board that includes a processor and multiple sensors. The board can display its information along with sensor readings.
- **Sensor Data Generation**: Randomly generates sensor readings for various types of sensors, including temperature, power, pressure, light, humidity, GPS, and more.
- **OpenAI GPT-4 Integration**: Sends user prompts to the GPT-4 model to get AI-generated responses based on a topic of interest.
- **Benchmarking**: Measures the time it takes to display information for all RISC-V boards.

## Requirements

To run this script, you need:

- Python 3.x
- OpenAI Python SDK (`openai` library)
- OpenAI API key (Ensure to set your OpenAI key securely)

You can install the required libraries with the following command:
```bash
pip install openai
```

## Usage

1. **RISC-V Processor and Board Simulation**: The script defines several RISC-V processors with GPU support and uses them to create RISC-V boards. Each board has random sensor data, which can be displayed along with processor information.

2. **Displaying Information**: To display information about all the boards and sensors, simply run the script and call the `display_boards_info()` function. This function also times the process of displaying the board information.

3. **ChatGPT Response**: The script integrates OpenAI's GPT-4 model to respond to user prompts. By default, it includes an example prompt: *"Describe the use of RISC-V processors in embedded systems."* The response from GPT-4 mni will be printed in the console.

## Code Components

### 1. OpenAI GPT-4 Integration
The script uses the OpenAI Python SDK to interact with GPT-4 mini, sending user-provided prompts and receiving AI-generated responses.

```python
def get_chatgpt_mini_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    return response.choices[0].message['content']
```

### 2. RISC-V Processor Class
Defines a RISC-V processor with attributes like name, clock speed, cores, power consumption, and GPU type.

```python
class RISCVProcessor:
    def __init__(self, name, clock_speed, cores, power_consumption, gpu):
        self.name = name
        self.clock_speed = clock_speed
        self.cores = cores
        self.power_consumption = power_consumption
        self.gpu = gpu

    def display_info(self):
        print(f"Processor: {self.name}")
        print(f"Clock Speed: {self.clock_speed} GHz")
        print(f"Cores: {self.cores}")
        print(f"Power Consumption: {self.power_consumption} Watts")
        print(f"GPU: {self.gpu}")
```

### 3. RISC-V Board Class
Each board includes a processor and a set of sensors, and it can display both the processor information and current sensor readings.

```python
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
```

### 4. Sensor Data Generation
Generates random sensor data for various types of sensors, which can be associated with each RISC-V board.

```python
def generate_sensor_data():
    return [
        {"type": "Temperature Sensor", "value": random.uniform(25.0, 80.0)},
        {"type": "Power Sensor", "value": random.uniform(10.0, 60.0)},
        ...
    ]
```

### 5. Benchmarking
Measures the time taken to display information for all the boards.

```python
def display_boards_info():
    start_time = time.time()
    for board in boards:
        board.display_info()
        print("-" * 40)
    elapsed_time = time.time() - start_time
    print(f"Benchmark: Displaying board info took {elapsed_time:.4f} seconds")
```

## Example Output

```bash
Board: Arduino Mega RISC-V
Processor: SiFive Freedom E300
Clock Speed: 1.6 GHz
Cores: 1
Power Consumption: 1.5 Watts
GPU: Mali-400 MP
Sensor: Temperature Sensor - Reading: 30.5
Sensor: Power Sensor - Reading: 15.3
...
Benchmark: Displaying board info took 0.1254 seconds
ChatGPT Response:
RISC-V processors are gaining popularity in embedded systems due to their...
```

## License

This project is licensed under the MIT License.

## Acknowledgments

- OpenAI for providing the GPT-4 model
- The RISC-V community for their contributions to open-source hardware