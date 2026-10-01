import subprocess
import time

def shutdown_laptop(delay_seconds=0):
    """Shutdown the laptop with optional delay"""
    
    # Steps: 
    # 1. Check if delay is specified
    # 2. Wait for the specified delay time
    # 3. Initiate system shutdown
    
    # Step-1: Check if delay is specified and wait if needed
    if delay_seconds > 0:
        print(f"Shutting down in {delay_seconds} seconds...")
        time.sleep(delay_seconds)
    
    # Step-2: Initiate system shutdown command
    try:
        subprocess.Popen(['shutdown', '/s', '/t', '0'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✓ Shutdown initiated")
    except Exception as e:
        print(f"✗ Failed to shutdown: {e}")

if __name__ == '__main__':
    shutdown_laptop()