# Recipe Shorts App

A web application that extracts recipe information from YouTube Shorts videos. The application transcribes the audio, uses AI to extract recipe details, and presents them in an organized, appealing format.

## Features

- YouTube Shorts video processing
- Audio transcription using OpenAI Whisper
- AI-powered recipe extraction using GPT-3.5
- Recipe storage and management
- Modern React frontend interface
- RESTful Flask backend API

## System Architecture

### Backend Components

1. **YouTube Service (`youtube.py`)**
   - Handles YouTube video URL validation and processing
   - Extracts video IDs from various YouTube URL formats
   - Fetches video transcripts using the YouTube Transcript API
   - Validates video URLs and transcript availability

2. **Recipe Extractor (`recipe_extractor.py`)**
   - Uses OpenAI's Whisper model for audio transcription
   - Leverages GPT-3.5 to extract structured recipe information
   - Processes transcripts to identify:
     - Recipe title
     - Ingredients list
     - Step-by-step instructions
     - Cooking time
     - Number of servings

3. **Storage Service (`storage.py`)**
   - Manages recipe data persistence using JSON storage
   - Provides CRUD operations for recipes
   - Maintains recipe metadata including creation timestamps
   - Handles data validation and error cases

4. **API Routes (`routes.py`)**
   - RESTful endpoints for recipe management:
     - `GET /recipes`: Retrieve all recipes
     - `POST /recipes/process`: Process new YouTube videos
     - `DELETE /recipes/<id>`: Remove recipes
   - Handles request validation and error responses
   - Manages API authentication and rate limiting

### Frontend Components

1. **React Application**
   - Built with Vite for optimal development experience
   - Uses Tailwind CSS for modern, responsive styling
   - Implements a clean, intuitive user interface

2. **Key Features**
   - Video URL input and validation
   - Recipe display with organized sections
   - Navigation between multiple recipes
   - Recipe management (view/delete)
   - Responsive design for all devices

## Prerequisites

- Python 3.9 or higher
- Node.js 18 or higher
- Docker and Docker Compose (for containerized setup)
- OpenAI API key

## Setup Instructions

### Option 1: Docker Setup (Recommended)

1. Clone the repository:
```bash
git clone [repository-url]
cd youtube-to-recipe
```

2. Create a `.env` file in the root directory:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

3. Build and start the containers:
```bash
docker-compose up --build
```

4. Access the application:
- Frontend: http://localhost:5173
- Backend API: http://localhost:5000

### Option 2: Local Development Setup

1. Clone the repository:
```bash
git clone [repository-url]
cd recipe-shorts-app
```

2. Set up the backend:
```bash
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Unix/MacOS:
source venv/bin/activate
pip install -r requirements.txt
```

3. Set up the frontend:
```bash
cd frontend
npm install
```

4. Create a `.env` file in the backend directory:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

5. Start the application:
- For Windows, use the provided batch script:
```bash
start_app.bat
```
- For manual start:
  - Backend: `python run.py` (in the backend directory)
  - Frontend: `npm run dev` (in the frontend directory)

## Usage

1. Open the application in your browser (http://localhost:5173)
2. Paste a YouTube video URL into the input field
3. Click "Extract Recipe" to process the video
4. View the extracted recipe information
5. Navigate between recipes using the arrow buttons
6. Delete recipes using the delete button

## Development

### Project Structure
```
recipe-shorts-app/
├── backend/
│   ├── app/
│   │   ├── services/
│   │   │   ├── recipe_extractor.py    # AI-powered recipe extraction
│   │   │   ├── youtube.py            # YouTube video processing
│   │   │   └── storage.py            # Recipe data persistence
│   │   └── api/
│   │       └── routes.py             # API endpoints
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── src/
│   │   ├── App.jsx                   # Main application component
│   │   └── main.jsx                  # Application entry point
│   └── package.json
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
└── README.md
```

### API Endpoints

- `GET /api/recipes` - Get all recipes
- `POST /api/recipes/process` - Process a YouTube video and extract recipe
- `DELETE /api/recipes/<id>` - Delete a recipe

## Troubleshooting

1. If the backend fails to start:
   - Check if the OpenAI API key is correctly set in the `.env` file
   - Ensure port 5000 is not in use
   - Check Python virtual environment is activated

2. If the frontend fails to start:
   - Ensure Node.js is installed correctly
   - Check if port 5173 is not in use
   - Try clearing npm cache: `npm cache clean --force`

3. If Docker setup fails:
   - Ensure Docker and Docker Compose are installed
   - Check if ports 5000 and 5173 are available
   - Try rebuilding containers: `docker-compose up --build --force-recreate`

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
