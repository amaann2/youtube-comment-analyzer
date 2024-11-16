# Project Setup Guide

## Prerequisites:

Before starting the setup, ensure the following are installed on your system:

- Python 3.12.

## Step 1: Create .env File

In the root directory of your project, create a `.env` file to store environment variables.

## Step 2: Create new virtual environment

```
python -m venv .venv
```

## Step 3: Activate the virtual env

```
source .venv/bin/activate
```

## Step 4: Install All Dependencies

```
pip install -r requirements.txt
```

## Step 5: Run Server

From the `src` directory in your project folder, start the FastAPI server:

```
cd src
python server.py
```
