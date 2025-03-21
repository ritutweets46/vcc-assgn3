import psutil
import time
import logging
import subprocess
from typing import Tuple

# Configure logging
logging.basicConfig(
    filename='resource_usage.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

class ResourceMonitor:
    """Class to monitor system resources and handle scaling."""
   
    THRESHOLD = 75  # Resource usage threshold in percentage
    CHECK_INTERVAL = 10  # Time interval between checks in seconds
   
    @staticmethod
    def get_resource_usage() -> Tuple[float, float, float]:
        """Get current CPU, memory, and disk usage percentages."""
        cpu_usage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        mem_usage = memory.percent
        disk_usage = psutil.disk_usage('/').percent
        return cpu_usage, mem_usage, disk_usage
   
    @staticmethod
    def log_and_print_usage(cpu: float, mem: float, disk: float) -> None:
        """Log and print resource usage information."""
        message = f"CPU: {cpu}%, Memory: {mem}%, Disk: {disk}%"
        logging.info(message)
        print(message)
   
    @staticmethod
    def scale_to_gcp() -> bool:
        """Trigger scaling to GCP by creating an instance."""
        try:
            subprocess.run([
                "./google-cloud-sdk/bin/gcloud",
                "compute",
                "instances",
                "create",
                "gcp-instance",
                "--machine-type=e2-medium",
                "--zone=asia-south2-a"
            ], check=True)
            print("Successfully triggered GCP scaling.")
            return True
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to scale to GCP: {e}")
            print(f"Error scaling to GCP: {e}")
            return False
   
    def monitor_and_scale(self) -> None:
        """Monitor resources and trigger scaling if thresholds are exceeded."""
        while True:
            cpu, mem, disk = self.get_resource_usage()
            self.log_and_print_usage(cpu, mem, disk)
           
            if cpu > self.THRESHOLD or mem > self.THRESHOLD or disk > self.THRESHOLD:
                print("Resource threshold exceeded! Triggering cloud scaling...")
                self.scale_to_gcp()
                break
           
            time.sleep(self.CHECK_INTERVAL)

def main():
    """Main function to start resource monitoring."""
    monitor = ResourceMonitor()
    monitor.monitor_and_scale()

if __name__ == "__main__":
    main()
