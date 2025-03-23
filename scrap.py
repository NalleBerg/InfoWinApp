import winreg

def get_windows_license_key():
    try:
        # Open the registry key where the product ID is stored
        registry_key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows NT\CurrentVersion"
        )
        
        # Read the binary DigitalProductId value
        digital_product_id, _ = winreg.QueryValueEx(registry_key, "DigitalProductId")
        winreg.CloseKey(registry_key)
        
        # Decode the binary data into the product key
        charset = "BCDFGHJKMPQRTVWXY2346789"  # Valid characters for the key
        product_key = []
        
        # Decode the 25-character key from the binary data
        for i in range(24, -1, -1):
            digit = 0
            for j in range(14, -1, -1):
                digit = (digit << 8) | digital_product_id[52 + j]
                digital_product_id = bytearray(digital_product_id)
                digital_product_id[52 + j] = digit // 24
                digit %= 24
            product_key.append(charset[digit])
        
        # Format the key with dashes
        return '-'.join([''.join(product_key[::-1][i:i+5]) for i in range(0, 25, 5)])
    
    except Exception as e:
        return f"Error retrieving key: {e}"

# Print the result
winkey = get_windows_license_key()
print (winkey)