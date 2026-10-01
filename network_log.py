import subprocess
import csv
import os
from datetime import datetime

def get_csv_filename():
    """Generate CSV filename with current date and time in ddmmyyyy_hrmmss format"""
    current_time = datetime.now().strftime('%d%m%Y_%H%M%S')
    return f'network_log_{current_time}.csv'

def write_step_output(step_number, output_message, filename=None):
    """Write step execution output to CSV file with error handling"""
    if filename is None:
        filename = get_csv_filename()
    
    try:
        file_exists = os.path.isfile(filename)
        
        with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header if file is new
            if not file_exists:
                writer.writerow(['Step', 'Output'])
            
            writer.writerow([step_number, output_message])
            
            # Force flush to ensure data is written immediately
            csvfile.flush()
            
    except PermissionError:
        print(f"⚠ Warning: Permission denied to write to {filename}")
    except OSError as e:
        print(f"⚠ Warning: OS error while writing to CSV: {e}")
    except Exception as e:
        print(f"⚠ Warning: Failed to write to CSV file: {e}")

def check_network():
    """Perform network diagnostics with step-by-step logging"""
    
    # Steps: 
    # 1. Check Internet Connectivity
    # 2. Get Local IP Configuration
    # 3. Ping Google DNS
    # 4. Check WiFi Status
    # 5. Trace Route to Google
    
    csv_file = get_csv_filename()
    print(f"Logging to: {csv_file}\n")
    print("Starting network diagnostics...\n")
    
    success_count = 0
    total_steps = 5
    
    # Step-1: Check Internet Connectivity
    try:
        result = subprocess.run(['ping', '-n', '1', 'google.com'], 
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode == 0:
            message = "✓ Internet connection active"
        else:
            message = "✗ Internet connection failed"
        print(message)
        write_step_output(1, message, csv_file)
        if result.returncode == 0:
            success_count += 1
    except Exception as e:
        message = f"✗ Failed to check connectivity: {e}"
        print(message)
        write_step_output(1, message, csv_file)
    
    # Step-2: Get Local IP Configuration
    try:
        result = subprocess.run(['ipconfig'], 
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            message = "✓ IP configuration retrieved"
        else:
            message = "✗ Failed to retrieve IP configuration"
        print(message)
        write_step_output(2, message, csv_file)
        if result.returncode == 0:
            success_count += 1
    except Exception as e:
        message = f"✗ Failed to get IP config: {e}"
        print(message)
        write_step_output(2, message, csv_file)
    
    # Step-3: Ping Google DNS (8.8.8.8)
    try:
        result = subprocess.run(['ping', '-n', '1', '8.8.8.8'], 
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode == 0:
            message = "✓ Google DNS reachable"
        else:
            message = "✗ Google DNS unreachable"
        print(message)
        write_step_output(3, message, csv_file)
        if result.returncode == 0:
            success_count += 1
    except Exception as e:
        message = f"✗ Failed to ping DNS: {e}"
        print(message)
        write_step_output(3, message, csv_file)
    
    # Step-4: Check WiFi Status
    try:
        result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], 
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if "State" in result.stdout and "connected" in result.stdout.lower():
            message = "✓ WiFi is connected"
        else:
            message = "⚠ WiFi is not connected or not available"
        print(message)
        write_step_output(4, message, csv_file)
        success_count += 1
    except Exception as e:
        message = f"✗ Failed to check WiFi status: {e}"
        print(message)
        write_step_output(4, message, csv_file)
    
    # Step-5: Trace Route to Google
    try:
        # Using -d to resolve addresses and -h 4 for max 4 hops for speed
        result = subprocess.run(['tracert', '-d', '-h', '4', 'google.com'], 
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode == 0:
            message = "✓ Trace route completed"
        else:
            message = "⚠ Trace route failed or timed out"
        print(message)
        write_step_output(5, message, csv_file)
        if result.returncode == 0:
            success_count += 1
    except Exception as e:
        message = f"✗ Failed to trace route: {e}"
        print(message)
        write_step_output(5, message, csv_file)
    
    # Overall Output with actual status
    if success_count == total_steps:
        overall_message = f"\n✓ All {total_steps} network checks completed successfully!"
    elif success_count == 0:
        overall_message = f"\n✗ Failed to perform any network checks (0/{total_steps})"
    else:
        overall_message = f"\n⚠ Partially successful: {success_count}/{total_steps} network checks done"
    
    print(overall_message)
    write_step_output('Overall', overall_message, csv_file)

if __name__ == '__main__':
    check_network()