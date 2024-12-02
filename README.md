# Text Summarization Web Application

This project is a Flask web application that allows users to generate abstract summaries from input text. It uses the T5 Small fine-tuned Hugging Face model, implemented with PyTorch Lightning, to perform text summarization. The model is stored and retrieved from an S3 bucket for efficient management.

---

## Table of Contents

1. [Installation](#installation)
2. [Running the Application](#running-the-application)
3. [Web Interface](#web-interface)
4. [Model Training and Fine-Tuning](#model-training-and-fine-tuning)
5. [S3 Bucket Integration](#s3-bucket-integration)
6. [Dependencies](#dependencies)
7. [License](#license)

---

## Installation

Follow these steps to set up the project locally:

1. **Clone the repository:**

   ```bash
   git clone <repository_url>
   cd text-summarization-webapp

2. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt

3. **Set up environment variables for AWS S3 (you'll need to configure AWS credentials for this project):**
    
    ```bash
    AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY
    AWS_BUCKET_NAME

## Running the Application

   **Start the Flask Application: After installing dependencies, start the Flask app by running:**
      ```python app.py```

   The Flask app will be available at 
    ```http://127.0.0.1:5000.```
    Open this URL in your browser.

## Web Interface Home Page

  **The home page provides a simple text input form where users can enter the text they want to summarize. The user can click the "Summarize" button to generate the abstract summary.** 
  
  How It Works

   The user enters a block of text into the form.
   The text is sent to the Flask backend, where it is processed by the T5 Small model.
   The model generates an abstract summary and displays it on the web page.

## Model Training and Fine-Tuning

  **The T5 model used in this project is fine-tuned for text summarization. Fine-tuning is done using the Hugging Face transformers library along with PyTorch Lightning.** 
    
   Steps for Fine-Tuning:

      Prepare Dataset: We use a summarization dataset (e.g., CNN/Daily Mail) to fine-tune the model.
      Train the Model: The T5 Small model is fine-tuned using PyTorch Lightning for efficient model training.
      Save the Model: After training, the fine-tuned model is saved to an S3 bucket for easy retrieval.

## S3 Bucket Integration

   **The trained model is saved to and loaded from an S3 bucket, enabling scalable model storage and retrieval. This setup is ideal for deploying models in production environments.** 
   Saving the Model to S3:

   After fine-tuning, the model is saved to the S3 bucket:
    ```
    import boto3 import torch
    def save_model_to_s3(model, model_name, bucket_name): s3 = boto3.client('s3') model.save_pretrained(model_name) s3.upload_file(model_name, bucket_name, model_name)
    ```
    
    
   Loading the Model from S3:

   When the Flask app runs, it loads the model from the S3 bucket for inference:

   ```
     def load_model_from_s3(model_name, bucket_name): s3 = boto3.client('s3') s3.download_file(bucket_name, model_name, model_name) model = T5ForConditionalGeneration.from_pretrained(model_name) return model
   ```

## Dependencies

   The following libraries are required to run the project:

    flask: The web framework for the Flask application.
    transformers: Hugging Face library to load the T5 model.
    torch: PyTorch library used for model training and inference.
    pytorch-lightning: For efficient model training.
    boto3: AWS SDK for interacting with S3.
    requests: To handle web requests and model inference.

## Install all dependencies using:

```pip install -r requirements.txt```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
