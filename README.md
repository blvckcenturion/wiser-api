## Wiser - A Youtube Transcription and Summarization App

This project is a web application that allows users to transcribe and summarize YouTube videos. It utilizes OpenAI and Langchain technologies to accomplish this functionality. The app consists of four main components: a bucket on Google Cloud Storage, a MySQL database, a frontend web app, and an API.

---

## Components
### 1. Google Cloud Storage Bucket
The Google Cloud Storage bucket is used to store the transcriptions and summarizations of the YouTube videos. The app uploads and retrieves the processed data from this bucket, ensuring secure and reliable storage.

### 2. MySQL Database
The MySQL database is utilized to keep a record of the summarizations and users in the app. It stores relevant information such as user profiles, video metadata, and summary data. The database allows for efficient data management and retrieval.

### 3. Frontend Web App (NextJS + TailwindCSS + TypeScript)
The frontend web app provides a user-friendly interface for interacting with the API and accessing the transcriptions and summarizations. Users can submit YouTube video URLs, view the processed results, and manage their account settings. The web app is designed to be intuitive and responsive, offering a seamless user experience.

### 4. API (Python + FastAPI + LangChain)
The API is responsible for handling the transcription and summarization tasks. It integrates with OpenAI and Langchain technologies to process the YouTube videos and generate accurate transcriptions and summaries. The API follows RESTful principles and provides endpoints for video submission, retrieval of processed data, and user authentication.

---

## Installation

1. Clone the repository.
2. Install the necessary dependencies for both the frontend and backend components.
3. Configure the API credentials and environment variables.
4. Set up the MySQL database and ensure the connection details are correctly configured.
5. Run the backend API server.
6. Start the frontend web app.

---

## Creator
- Santiago Sarabia
