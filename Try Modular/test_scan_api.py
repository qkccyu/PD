#!/usr/bin/env python3
"""
Test Scan API
This script tests the scan API directly to help debug the issue.
"""

import requests
import os
from io import BytesIO
from PIL import Image

def test_scan_api():
    # Create a test image
    print("Creating a test image...")
    img = Image.new('RGB', (300, 300), color='red')
    img_bytes = BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    # Prepare the data
    files = {
        'image': ('test_image.jpg', img_bytes, 'image/jpeg')
    }
    
    data = {
        'patient_name': 'Test Patient',
        'notes': 'Test scan via API',
        'condition': 'Onychomycosis',
        'severity': 'Mild'
    }
    
    print("Testing scan API...")
    print(f"Data: {data}")
    print(f"Image: test_image.jpg")
    
    try:
        response = requests.post('http://localhost:5000/api/scans', files=files, data=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("SUCCESS: Scan saved successfully!")
        else:
            print("ERROR: Scan failed to save")
            
    except Exception as e:
        print(f"ERROR: Could not connect to server: {e}")
        print("Make sure the Flask server is running on localhost:5000")

if __name__ == "__main__":
    test_scan_api()