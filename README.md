# Tangerine - Ayurvedic Practitioners App

A React Native Expo app with FastAPI backend for finding and booking Ayurvedic practitioners.

## Architecture

- **Frontend**: React Native with Expo Router
- **Backend**: FastAPI (Python) - serves practitioner data only
- **Data Flow**: Home page fetches practitioners from API, rest of the app runs client-side

## Setup Instructions

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the FastAPI server**:
   ```bash
   python start.py
   ```
   
   The API will be available at `http://localhost:8000`

4. **API Documentation**:
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

### Frontend Setup

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Update API URL**:
   - Find your local IP address (not localhost/127.0.0.1)
   - Update `services/api.ts` line 8 with your IP:
     ```typescript
     const developmentUrl = 'http://YOUR_IP_ADDRESS:8000';
     ```

3. **Start the Expo development server**:
   ```bash
   npm run dev
   ```

## API Endpoints

- `GET /api/practitioners` - Get all practitioners
- `GET /api/practitioners/{id}` - Get practitioner by ID
- `GET /api/practitioners/search?q={query}` - Search practitioners
- `GET /health` - Health check

## Project Structure

```
├── app/                    # React Native screens
│   ├── (tabs)/            # Tab navigation screens
│   │   └── index.tsx      # Home screen (uses API)
│   └── book/              # Booking screens
├── backend/               # FastAPI backend
│   ├── main.py           # FastAPI app
│   ├── models.py         # Pydantic models
│   ├── database.py       # Mock database
│   └── start.py          # Startup script
├── services/             # API client services
├── hooks/                # Custom React hooks
└── types/                # TypeScript type definitions
```

## Development Notes

- The backend only serves practitioner data for the home page
- All other app functionality (booking, scheduling, etc.) remains client-side
- The app gracefully handles API errors and network issues
- Loading states and error handling are implemented throughout

## Deployment

### Backend Deployment
- Deploy FastAPI to platforms like Railway, Render, or Heroku
- Update frontend API URL to production endpoint

### Frontend Deployment
- Build for web: `npm run build:web`
- Build for mobile: Use EAS Build for app stores

## Environment Variables

### Frontend (.env)
```
EXPO_PUBLIC_API_URL=http://localhost:8000
EXPO_PUBLIC_ENVIRONMENT=development
```

### Backend (backend/.env)
```
PORT=8000
ENVIRONMENT=development
```