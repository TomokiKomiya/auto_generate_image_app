# AI-Powered House Image Generator and Social Media Poster

This Python script generates images of houses based on random architectural styles, house types, and price ranges using OpenAI's DALL-E API. The generated images are described using OpenAI's GPT model and automatically posted on Threads via the Meta API.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)

## Introduction

This project leverages OpenAI's DALL-E and GPT-4 models to generate realistic images of houses with varying architectural styles, and then publishes these images along with a descriptive caption to Threads, a social media platform. The script is designed to automate the entire process, from image generation to social media posting.

## Features

- **Image Generation**: Automatically generates images of houses based on random parameters using OpenAI's DALL-E API.
- **Image Description**: Uses GPT-4 to create detailed descriptions of the generated images suitable for social media posts.
- **Cloud Storage**: Saves the generated images to Google Cloud Storage for easy access and management.
- **Social Media Posting**: Posts the generated images along with their descriptions to Threads via the Meta API.
- **Randomized Content**: Randomly selects house types, architectural styles, and price ranges to create diverse content.

## Installation

### Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or higher
- pip (Python package installer)
- Google Cloud SDK (for Google Cloud Storage)
- OpenAI API Key
- Threads API Access Token

### Setup

1. Clone the repository:
   ```bash
   git clone git@github.com:TomokiKomiya/auto_generate_image_app.git
   cd auto_generate_image_app
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up Google Cloud Storage:
   - Ensure you have a Google Cloud project with billing enabled.
   - Create a Cloud Storage bucket where the images will be stored.
   - Download your service account key and set the environment variable `GOOGLE_APPLICATION_CREDENTIALS` to the path of this key.

## Usage

1. **Configure Environment Variables**: Create a `.env` file in the project root and add the necessary environment variables as described in the [Environment Variables](#environment-variables) section.

2. **Run the Script**:
   ```bash
   python main.py
   ```

   The script will randomly generate an image, describe it, upload it to Google Cloud Storage, and post it on Threads.

3. **Output**: Check the terminal for the image URL and confirmation that the post was published successfully.

