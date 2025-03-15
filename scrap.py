import subprocess

    def get_processor_name():
        try:
            # Use PowerShell to get the processor name
            command = 'powershell -command "Get-WmiObject Win32_Processor | Select-Object -ExpandProperty Name"'
            output = subprocess.check_output(
                command, 
                shell=True, 
                stderr=subprocess.STDOUT, 
                universal_newlines=True
            )
            
            # Extract the processor name from the output
            processor_name = output.strip()
            return processor_name
        except Exception as e:
            print(f"Error retrieving processor name: {e}")
            return "Unknown"

def main():
    processor_name = get_processor_name()
    print(f"Processor: {processor_name}")

if __name__ == "__main__":
    main()