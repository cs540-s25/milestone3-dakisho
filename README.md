# Movie Discovery App

A full-stack web application for movie discovery, allowing users to view movie details, rate movies, and leave comments.

## Features
1. User authentication (signup and login)
2. Randomly displayed movies from a curated list
3. Movie data fetched from TMDB API:
   - Movie title, tagline, genres, and poster image
   - Wikipedia link for additional information
4. User ratings and comments:
   - Rate movies on a scale from 1-10
   - Leave optional comments with ratings
   - View all ratings and comments from other users
5. React frontend with client-side processing:
   - Edit and delete your ratings
   - Save changes without page refresh
   - Modern, responsive UI

---

## Local Setup

### Backend Setup

1. **Clone** this repo:
   ```bash
   git clone https://github.com/cs540-s25/milestone3-dakisho.git
   cd milestone3-dakisho
   ```

2. **Install Backend Dependencies**:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Set Environment Variables**:
   - Create a `.env` file in the root directory with the following variables:
   ```
   TMDB_API_KEY=your_tmdb_api_key
   SECRET_KEY=your_secret_key
   DATABASE_URL=sqlite:///app.db
   ```

4. Run the initial build script:
   ```
   chmod +x ./build.sh && ./build.sh
   ```

4. **Run the Flask API Backend**:
   ```bash
   python -m src.main
   ```
   This will start the backend server at [http://localhost:8080](http://localhost:8080).


---

## Code Formatting

### Python (Backend)
This project uses Black for Python code formatting.

```bash
black src/
```

### JavaScript (Frontend)
This project uses ESLint with Airbnb rules for JavaScript code formatting.

```bash
cd frontend
npm run lint
```

---

