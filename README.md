# Japanese-English Diary Application

A bilingual diary application that allows users to write diary entries in Japanese, automatically translates them to English, and provides features to save favorite expressions.

## Features

- Simple text-based diary entry system
- Automatic translation of Japanese entries to English
- Side-by-side view of Japanese and English content
- Ability to select and save interesting expressions or idioms
- In-memory database for storing diary entries and favorite expressions

## Tech Stack

- **Backend**: FastAPI with RESTful API endpoints
- **Frontend**: React with TypeScript and Shadcn UI components
- **Translation**: deep-translator library for Japanese to English translation
- **Data Storage**: In-memory database (for prototyping)

## Getting Started

### Prerequisites

- Python 3.12+
- Node.js 18+
- Poetry (for Python dependency management)
- npm (for JavaScript dependency management)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/kwgch/devin-tutorial.git
   cd devin-tutorial
   ```

2. Install backend dependencies:
   ```bash
   cd backend
   poetry install
   ```

3. Install frontend dependencies:
   ```bash
   cd ../frontend
   npm install
   ```

### Running the Application

1. Start the backend server:
   ```bash
   cd backend
   poetry run uvicorn app.main:app --reload
   ```

2. Start the frontend development server:
   ```bash
   cd frontend
   npm run dev
   ```

3. Open your browser and navigate to:
   ```
   http://localhost:5173
   ```

## How to Use

1. **Write a Diary Entry**:
   - Enter your diary content in Japanese in the text area
   - Click "保存して翻訳" (Save and Translate) to save your entry

2. **View Entries**:
   - All diary entries are displayed in the diary list
   - Each entry shows both Japanese text and its English translation

3. **View Entry Details**:
   - Click on any entry to view it in detail
   - The detail view shows Japanese and English text side by side

4. **Save Favorite Expressions**:
   - In the detail view, select text in the Japanese section
   - Select the corresponding text in the English section
   - Add an optional note about the expression
   - Click "表現を保存" (Save Expression) to save it

5. **View Saved Expressions**:
   - All saved expressions are displayed in the sidebar
   - Each expression shows both Japanese and English text, along with any notes

## API Endpoints

- `GET /api/diary`: Get all diary entries
- `POST /api/diary`: Create a new diary entry
- `GET /api/diary/{entry_id}`: Get a specific diary entry
- `PUT /api/diary/{entry_id}`: Update a diary entry
- `DELETE /api/diary/{entry_id}`: Delete a diary entry
- `POST /api/diary/{entry_id}/favorite`: Add a favorite expression
- `GET /api/favorites`: Get all favorite expressions
