from flask import Flask, request, render_template, redirect, url_for
import boto3

app = Flask(__name__)

# Set your AWS credentials and bucket name
AWS_ACCESS_KEY_ID = 'Your access key'
AWS_SECRET_ACCESS_KEY = 'Your secret key'
AWS_REGION = 'us-east-1'
S3_BUCKET = 's3 bucket name'

# Initialize the S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

@app.route('/')
def index():
    # Serve the HTML form
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Get the uploaded files from the form
    files = request.files.getlist('files')
    
    # List to store error lines
    error_lines = []
    
    # Process each file and extract error lines
    for file in files:
        lines = file.readlines()
        for line in lines:
            line = line.decode('utf-8')
            # Check if the line contains the word "error"
            if 'error' in line.lower():
                error_lines.append(line)
    
    # Create a file with error lines
    error_file_content = "".join(error_lines)
    error_file_name = 'error_log.txt'
    
    # Upload the error file to S3
    s3_client.put_object(Bucket=S3_BUCKET, Key=error_file_name, Body=error_file_content, ACL='public-read')

    
    # Generate the S3 file URL
    file_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{error_file_name}"
    
    # Redirect to the download page
    return redirect(url_for('download', file_url=file_url))

@app.route('/download')
def download():
    # Get the file URL from the query parameter
    file_url = request.args.get('file_url')
    
    # Serve the download button and file link
    return render_template('download.html', file_url=file_url)

if __name__ == '__main__':
    app.run(debug=True)
