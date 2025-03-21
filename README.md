# Cloud-Powered Auto-Updating Visualizations

Cloud-Powered Auto-Updating Visualizations is an automated financial data visualization tool that gathers historical stock data, processes it using Python and pandas, and creates insightful visualizations with Matplotlib. The project leverages cloud services—AWS S3 for file storage and AWS EC2 (with cron scheduling) for automation—to ensure that the visualizations are updated periodically without manual intervention.

# Table of Contents:

  Overview
  Features
  Architecture
  Setup and Installation
  Usage
  AWS Integration
  Uploading Visualizations to S3
  Automating Updates with EC2 and Cron

# Overview:

Cloud-Powered Auto-Updating Visualizations demonstrates how to create dynamic, automatically updating data visualizations using a combination of Python, cloud APIs, and AWS services. The project retrieves historical stock prices for major banks (JPM, BAC, C, WFC, GS) via Twelve Data’s free API, processes the data into a consolidated pandas DataFrame, and then generates visualizations (e.g., boxplots) using Matplotlib.

# Features:

  Data Acquisition:
  Fetches 5-year historical daily stock prices for selected banks using the Twelve Data API.

  Data Processing:
  Utilizes pandas to parse JSON data, filter it, and format it for visualization.

  Data Visualization:
  Creates beautiful visualizations with Matplotlib, including boxplots that highlight data distribution and trends.

  Cloud Integration:
    AWS S3: Automatically uploads the generated PNG files to an S3 bucket for public access.
    AWS EC2: Schedules the script to run periodically using cron, ensuring the visualizations are always up-to-date.
  
  Automation:
  The process is fully automated—from data fetching and visualization generation to cloud uploading and scheduling.

# Architecture:

1. Data Layer:
  Fetches data from Twelve Data API.
  Processes data with Python and pandas.

2. Visualization Layer:
  Creates charts (boxplots) using Matplotlib.
  Saves visualizations as PNG files.

3. Cloud & Automation Layer:
  Uses boto3 to upload PNG files to an AWS S3 bucket.
  Deploys a Python script on an AWS EC2 instance, scheduled via cron to run periodically.

# Setup and Installation:

  Prerequisites:
    Python 3.x
    AWS Account (Free Tier eligible)
    Twelve Data API Key (free tier available)
    AWS CLI (configured with your credentials)
    Git
  
  Install Dependencies
    It's recommended to use a virtual environment:
    
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

  
  requirements.txt should include:
      pandas
      matplotlib
      requests
      boto3
        
# Usage:

  Run the script locally to generate the visualization:  
  
    python3 auto_update.py    
    
  This script will: 
    Fetch and process stock data.
    Generate a boxplot (or other visualizations) from the data.
    Save the visualization as bank_data_boxplot.png.
    Upload the image to your specified AWS S3 bucket.
    
# AWS Integration:
  Uploading Visualizations to S3:
  The script uses boto3 to upload the generated PNG file to an AWS S3 bucket. Please make sure your bucket is configured with a policy to allow public read access. The upload code in the script is as follows:
  
    import boto3
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file('bank_data_boxplot.png', 'your-s3-bucket-name', 'bank_data_boxplot.png')
    print("File uploaded to S3 successfully.")
    
  Automating Updates with EC2 and Cron:
  To ensure your visualization stays current:
  
    1. Launch an AWS EC2 instance:
        Choose a free tier-eligible instance (e.g., Amazon Linux 2 AMI, t2.micro).
        Create a key pair and note the public IP address.      
    2. Transfer your script to EC2 using SCP:
        scp -i /path/to/your-key.pem auto_update.py ec2-user@<public-ip>:/home/ec2-user
    3. SSH into the instance and install dependencies:
        ssh -i /path/to/your-key.pem ec2-user@<public-ip>
        sudo yum update -y
        sudo yum install python3-pip -y
        pip3 install pandas matplotlib requests boto3
    4. Set up the Cron Job:
        Create a cron file (e.g., bank_stock_data.cron) with the following content:
        00 7 * * 7 python3 /home/ec2-user/auto_update.py
        Import the cron file:
        crontab bank_stock_data.cron
        crontab -l  # To verify the cron job has been added
