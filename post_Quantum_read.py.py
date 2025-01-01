Performance Analysis of Post-Quantum Signature Schemes

This repository contains a Python script that analyzes the performance of post-quantum signature schemes using different implementations: hardware-accelerated, software-based, and RISC-V architecture. The performance metrics include signing and verification times, along with energy consumption estimates.

Table of Contents

	•	Prerequisites
	•	Installation
	•	Usage
	•	Code Explanation
	•	Results Visualization
	•	License

Prerequisites

Before running the script, ensure you have the following:

	•	Python 3.x
	•	Libraries:
	•	matplotlib
	•	openai
	•	logging

You can install the required libraries using pip:

pip install matplotlib openai

Installation

	1.	Clone the repository:

git clone https://github.com/yourusername/performance-analysis.git
cd performance-analysis


	2.	Set your OpenAI API key in the environment variables:

export OPENAI_API_KEY='your_openai_api_key'



Usage

To run the performance analysis, simply execute the script:

python performance_analysis.py

The script will log performance metrics to performance_test.log and display the analysis results.

Code Explanation

Key Components

	•	OpenAI API Integration: The script utilizes OpenAI’s API for generating sample data.
	•	PerformanceBoard Class: This class is responsible for recording performance metrics (signing and verification times) for hardware, software, and RISC-V implementations.
	•	Signature and Verification Functions: Simulated functions for hardware-accelerated, software, and RISC-V implementations are included.
	•	Performance Analysis Function: The analyze_performance function runs multiple iterations of signing and verification, records the data, and computes statistics.

Example of Performance Measurement

# Simulated hardware accelerator functions
def hardware_accelerated_dilithium_sign(message):
    time.sleep(0.01)  # Simulate faster processing
    return f"dilithium_signature_{random.randint(1000, 9999)}"

Results Visualization

The results are visualized using histograms, displaying the time taken for signing and verification across different implementations. The script generates plots and saves them as performance_analysis_riscv.png.

Energy Reduction Estimates

The script simulates energy consumption reduction estimates for each implementation:

print(f"Energy Reduction for Dilithium (HW): {hw_energy_reduction_dilithium * 100:.2f}%")

License

This project is licensed under the MIT License - see the LICENSE file for details.

