import openai
import time
import json
import psutil
import logging
# Initialize OpenAI API client with your API key
openai.api_key = ""

class FineTuningManager:
    def create_fine_tuning_job(self, training_file_id):
        try:
            response = openai.FineTuning.create(training_file=training_file_id)
            logging.info(f"Created fine-tuning job: {response['id']}")
            print(f"Created fine-tuning job: {response['id']}")
        except Exception as e:
            logging.error(f"Error creating fine-tuning job: {str(e)}")
            print(f"Error creating fine-tuning job: {str(e)}")

    def create_fine_tuning_job_json(self, coding_prompts, filename='training_data.json'):
        try:
            with open(filename, 'w') as f:
                json.dump(coding_prompts, f, indent=4)
            logging.info(f"fine-tuning data saved to {filename}")
            print(f"fine-tuning data saved to {filename}")
        except Exception as e:
            logging.error(f"Error saving fine-tuning data: {str(e)}")
            print(f"Error saving fine-tuning data: {str(e)}")

    def list_fine_tuning_jobs(self):
        try:
            response = openai.FineTuning.list()
            logging.info("Listed fine-tuning jobs.")
            print("fine-tuning jobs:")
            for job in response['data']:
                print(f"ID: {job['id']}, Status: {job['status']}")
        except Exception as e:
            logging.error(f"Error listing fine-tuning jobs: {str(e)}")
            print(f"Error listing fine-tuning jobs: {str(e)}")

    def retrieve_fine_tune_state(self, job_id):
        try:
            response = openai.fineTuning.retrieve(id=job_id)
            logging.info(f"Job {job_id} state: {response['status']}")
            print(f"Job {job_id} state: {response['status']}")
        except Exception as e:
            logging.error(f"Error retrieving job state: {str(e)}")
            print(f"Error retrieving job state: {str(e)}")

    def cancel_fine_tuning_job(self, job_id):
        try:
            response = openai.FineTuning.cancel(id=job_id)
            logging.info(f"Cancelled fine-tuning job: {response['id']}")
            print(f"Cancelled fine-tuning job: {response['id']}")
        except Exception as e:
            logging.error(f"Error cancelling fine-tuning job: {str(e)}")
            print(f"Error cancelling fine-tuning job: {str(e)}")

    def list_fine_tuning_job_events(self, job_id):
        try:
            response = openai.fineTuning.list_events(id=job_id)
            logging.info(f"Events for job {job_id}:")
            print(f"Events for job {job_id}:")
            for event in response['data']:
                print(f"Event: {event['message']}")
        except Exception as e:
            logging.error(f"Error listing job events: {str(e)}")
            print(f"Error listing job events: {str(e)}")

    def delete_fine_tuned_model(self, model_id):
        try:
            response = openai.Model.delete(model=model_id)
            logging.info(f"Deleted model: {response['id']}")
            print(f"Deleted model: {response['id']}")
        except Exception as e:
            logging.error(f"Error deleting model: {str(e)}")
            print(f"Error deleting model: {str(e)}")

    def create_completion(self, model_id, messages, max_tokens=150, temperature=0.7):
        try:
            response = openai.ChatCompletion.create(
                model=model_id,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            logging.info(f"Completion: {response['choices'][0]['message']['content']}")
            print(f"Completion: {response['choices'][0]['message']['content']}")
            return response['choices'][0]['message']['content']
        except Exception as e:
            logging.error(f"Error creating completion: {str(e)}")
            print(f"Error creating completion: {str(e)}")
            return None

    def get_sensor_data(self):
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        return {
            "cpu_usage": cpu_usage,
            "memory_total": memory_info.total,
            "memory_used": memory_info.used,
            "memory_free": memory_info.free
        }

    def monitor_resources(self):
        print("Monitoring resources...")
        try:
            while True:
                sensor_data = self.get_sensor_data()
                print(f"CPU Usage: {sensor_data['cpu_usage']}%")
                print(f"Memory Used: {sensor_data['memory_used'] / (1024 ** 2):.2f} MB")
                print(f"Memory Free: {sensor_data['memory_free'] / (1024 ** 2):.2f} MB")
                time.sleep(5)  # Update every 5 seconds
        except KeyboardInterrupt:
            print("Resource monitoring stopped.")

    def list_available_models(self):
        try:
            response = openai.Model.list()
            print("Available models:")
            for model in response['data']:
                print(f"Model ID: {model['id']}, Type: {model['object']}")
        except Exception as e:
            logging.error(f"Error listing available models: {str(e)}")
            print(f"Error listing available models: {str(e)}")

# Example usage
if __name__ == "__main__":
    manager = 'FineTuningManager'()

    # Example training file and model IDs
    training_file_id = "file-abc123"  # Example training file ID
    job_id = "ftjob-abc123"  # Provided job ID
    model_id = "gpt-4.0-turbo"  # ChatGPT-4.0 Mini model ID

    # Generate fine-tuning data (mock data for example)
    coding_prompts = [
        {
            "prompt": "How do I implement a simple RISC-V assembly loop?",
            "completion": "Here is an example of a RISC-V assembly loop:\n\n```\n"
                          "loop:\n"
                          "    addi t0, t0, 1\n"
                          "    bne t0, t1, loop\n"
                          "```"
        },
        {
            "prompt": "What is the purpose of the RISC-V `beq` instruction?",
            "completion": "The `beq` instruction is used to branch to a specified address if two registers are equal."
        }
    ]

    # Save fine-tuning data to JSON
    manager.create_fine_tuning_job_json(coding_prompts)

    # Create a fine-tuning job
    manager.create_fine_tuning_job(training_file_id)

    # List fine-tuning jobs
    manager.list_fine_tuning_jobs()

    # Retrieve the state of the fine-tune job
    manager.retrieve_fine_tune_state(job_id)

    # Cancel the fine-tuning job (optional if needed)
    # manager.cancel_fine_tuning_job(job_id)

    # List events from the fine-tuning job
    manager.list_fine_tuning_job_events(job_id)

    # Delete the fine-tuned model (if necessary)
    # manager.delete_fine_tuned_model(model_id)

    # Create a completion using the fine-tuned GPT-4 Mini model with RISC-V information
    manager.create_completion(model_id, [
        {"role": "system", "content": "Sure, here is information about RISC-V."},
        {"role": "user", "content": "What is the difference between RISC-V and ARM?"}
    ], max_tokens=300, temperature=0.6)

    # Monitor system resources
    # Uncomment to start monitoring
    # manager.monitor_resources()

    # List available models
    manager.list_available_models()


class FineTuningManager:
    def create_fine_tuning_job(self, training_file_id):
        try:
            response = openai.FineTuning.create(training_file=training_file_id)
            logging.info(f"Created fine-tuning job: {response['id']}")
            print(f"Created fine-tuning job: {response['id']}")
        except Exception as e:
            logging.error(f"Error creating fine-tuning job: {str(e)}")
            print(f"Error creating fine-tuning job: {str(e)}")

    def create_fine_tuning_job_json(self, coding_prompts, filename='training_data.json'):
        try:
            with open(filename, 'w') as f:
                json.dump(coding_prompts, f, indent=4)
            logging.info(f"fine-tuning data saved to {filename}")
            print(f"fine-tuning data saved to {filename}")
        except Exception as e:
            logging.error(f"Error saving fine-tuning data: {str(e)}")
            print(f"Error saving fine-tuning data: {str(e)}")

    def list_fine_tuning_jobs(self):
        try:
            response = openai.FineTuning.list()
            logging.info("Listed fine-tuning jobs.")
            print("fine-tuning jobs:")
            for job in response['data']:
                print(f"ID: {job['id']}, Status: {job['status']}")
        except Exception as e:
            logging.error(f"Error listing fine-tuning jobs: {str(e)}")
            print(f"Error listing fine-tuning jobs: {str(e)}")

    def retrieve_fine_tune_state(self, job_id):
        try:
            response = openai.fineTuning.retrieve(id=job_id)
            logging.info(f"Job {job_id} state: {response['status']}")
            print(f"Job {job_id} state: {response['status']}")
        except Exception as e:
            logging.error(f"Error retrieving job state: {str(e)}")
            print(f"Error retrieving job state: {str(e)}")

    def cancel_fine_tuning_job(self, job_id):
        try:
            response = openai.FineTuning.cancel(id=job_id)
            logging.info(f"Cancelled fine-tuning job: {response['id']}")
            print(f"Cancelled fine-tuning job: {response['id']}")
        except Exception as e:
            logging.error(f"Error cancelling fine-tuning job: {str(e)}")
            print(f"Error cancelling fine-tuning job: {str(e)}")

    def list_fine_tuning_job_events(self, job_id):
        try:
            response = openai.fineTuning.list_events(id=job_id)
            logging.info(f"Events for job {job_id}:")
            print(f"Events for job {job_id}:")
            for event in response['data']:
                print(f"Event: {event['message']}")
        except Exception as e:
            logging.error(f"Error listing job events: {str(e)}")
            print(f"Error listing job events: {str(e)}")

    def delete_fine_tuned_model(self, model_id):
        try:
            response = openai.Model.delete(model=model_id)
            logging.info(f"Deleted model: {response['id']}")
            print(f"Deleted model: {response['id']}")
        except Exception as e:
            logging.error(f"Error deleting model: {str(e)}")
            print(f"Error deleting model: {str(e)}")

    def create_completion(self, model_id, messages, max_tokens=150, temperature=0.7):
        try:
            response = openai.ChatCompletion.create(
                model=model_id,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            logging.info(f"Completion: {response['choices'][0]['message']['content']}")
            print(f"Completion: {response['choices'][0]['message']['content']}")
            return response['choices'][0]['message']['content']
        except Exception as e:
            logging.error(f"Error creating completion: {str(e)}")
            print(f"Error creating completion: {str(e)}")
            return None

    def get_sensor_data(self):
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        return {
            "cpu_usage": cpu_usage,
            "memory_total": memory_info.total,
            "memory_used": memory_info.used,
            "memory_free": memory_info.free
        }

    def monitor_resources(self):
        print("Monitoring resources...")
        try:
            while True:
                sensor_data = self.get_sensor_data()
                print(f"CPU Usage: {sensor_data['cpu_usage']}%")
                print(f"Memory Used: {sensor_data['memory_used'] / (1024 ** 2):.2f} MB")
                print(f"Memory Free: {sensor_data['memory_free'] / (1024 ** 2):.2f} MB")
                time.sleep(5)  # Update every 5 seconds
        except KeyboardInterrupt:
            print("Resource monitoring stopped.")

    def list_available_models(self):
        try:
            response = openai.Model.list()
            print("Available models:")
            for model in response['data']:
                print(f"Model ID: {model['id']}, Type: {model['object']}")
        except Exception as e:
            logging.error(f"Error listing available models: {str(e)}")
            print(f"Error listing available models: {str(e)}")

# Example usage
if __name__ == "__main__":
    manager = 'FineTuningManager'()

    # Example training file and model IDs
    training_file_id = "file-abc123"  # Example training file ID
    job_id = "ftjob-abc123"  # Provided job ID
    model_id = "gpt-4.0-turbo"  # ChatGPT-4.0 Mini model ID

    # Generate fine-tuning data (mock data for example)
    coding_prompts = [
        {
            "prompt": "How do I implement a simple RISC-V assembly loop?",
            "completion": "Here is an example of a RISC-V assembly loop:\n\n```\n"
                          "loop:\n"
                          "    addi t0, t0, 1\n"
                          "    bne t0, t1, loop\n"
                          "```"
        },
        {
            "prompt": "What is the purpose of the RISC-V `beq` instruction?",
            "completion": "The `beq` instruction is used to branch to a specified address if two registers are equal."
        }
    ]

    # Save fine-tuning data to JSON
    manager.create_fine_tuning_job_json(coding_prompts)

    # Create a fine-tuning job
    manager.create_fine_tuning_job(training_file_id)

    # List fine-tuning jobs
    manager.list_fine_tuning_jobs()

    # Retrieve the state of the fine-tune job
    manager.retrieve_fine_tune_state(job_id)

    # Cancel the fine-tuning job (optional if needed)
    # manager.cancel_fine_tuning_job(job_id)

    # List events from the fine-tuning job
    manager.list_fine_tuning_job_events(job_id)

    # Delete the fine-tuned model (if necessary)
    # manager.delete_fine_tuned_model(model_id)

    # Create a completion using the fine-tuned GPT-4 Mini model with RISC-V information
    manager.create_completion(model_id, [
        {"role": "system", "content": "Sure, here is information about RISC-V."},
        {"role": "user", "content": "What is the difference between RISC-V and ARM?"}
    ], max_tokens=300, temperature=0.6)

    # Monitor system resources
    # Uncomment to start monitoring
    # manager.monitor_resources()

    # List available models
    manager.list_available_models()