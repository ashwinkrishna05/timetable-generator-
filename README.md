# School Timetable Generator

A comprehensive web application for generating and managing school timetables with a modern Python FastAPI backend and Next.js frontend.

## Features

- **School Management**: Create and manage school profiles with board-specific curricula
- **Class Management**: Add classes with sections and stream selection (Science, Commerce, Arts)
- **Subject Management**: Board-based subjects for classes 1-10, stream-based for 11-12
- **Teacher Management**: Add teachers with subject and class assignments
- **Timetable Generation**: AI-powered timetable generation with constraints
- **Physical Education Limitation**: PE limited to 2 periods per week
- **Teacher Workload Analysis**: Monitor teacher workload and distribution
- **Substitution System**: Find substitute teachers based on availability
- **Export Functionality**: Export timetables in multiple formats
- **Modern UI**: Responsive design with Tailwind CSS

## Architecture

- **Backend**: Python FastAPI with SQLAlchemy ORM
- **Frontend**: Next.js 14 with TypeScript and Tailwind CSS
- **Database**: SQLite (default) or PostgreSQL
- **Authentication**: JWT-based authentication
- **State Management**: React Query for server state

## Prerequisites

- Python 3.8+
- Node.js 18+
- pip
- npm or yarn

## Installation

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run the backend**:
   ```bash
   python main.py
   ```
   
   The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Run the development server**:
   ```bash
   npm run dev
   # or
   yarn dev
   ```
   
   The frontend will be available at `http://localhost:3000`

## API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/token` - User login
- `GET /api/auth/me` - Get current user info

### Schools
- `POST /api/schools/` - Create school
- `GET /api/schools/` - List schools
- `GET /api/schools/{id}` - Get school details
- `PUT /api/schools/{id}` - Update school
- `DELETE /api/schools/{id}` - Delete school

### Classes
- `POST /api/classes/` - Create class
- `GET /api/classes/` - List classes
- `GET /api/classes/{id}` - Get class details
- `PUT /api/classes/{id}` - Update class
- `DELETE /api/classes/{id}` - Delete class

### Teachers
- `POST /api/teachers/` - Create teacher
- `GET /api/teachers/` - List teachers
- `GET /api/teachers/{id}` - Get teacher details
- `PUT /api/teachers/{id}` - Update teacher
- `DELETE /api/teachers/{id}` - Delete teacher

### Timetables
- `POST /api/timetables/generate` - Generate timetables
- `GET /api/timetables/class/{id}` - Get class timetable
- `GET /api/timetables/teacher/{id}/workload` - Get teacher workload
- `POST /api/timetables/substitute` - Find substitute teachers
- `GET /api/timetables/export/{id}` - Export timetable

## Usage

### 1. School Setup
1. Create a school profile with board selection (CBSE, ICSE, State Board)
2. Set regional language and working days
3. Configure timings for primary, secondary, and senior secondary classes

### 2. Class Management
1. Add classes with appropriate sections
2. For classes 11-12, select stream (Science, Commerce, Arts)
3. Configure ECA and lab activities if needed

### 3. Subject Assignment
1. Subjects are automatically assigned based on board and stream
2. Customize subject selection as needed
3. Set up ECA and lab schedules

### 4. Teacher Management
1. Add teachers with employee IDs
2. Assign subjects and classes to teachers
3. Monitor teacher workload distribution

### 5. Timetable Generation
1. Generate timetables for all classes
2. Physical Education is automatically limited to 2 periods per week
3. Review and export timetables

## Database Schema

The application uses the following main entities:
- **Schools**: School information and configuration
- **Classes**: Class details with sections and streams
- **Subjects**: Subject definitions with types and streams
- **Teachers**: Teacher information and qualifications
- **Timetables**: Generated timetable data
- **ECAs**: Extra-curricular activity schedules
- **Labs**: Laboratory activity schedules

## Configuration

### Backend Configuration
- Database URL (SQLite/PostgreSQL)
- JWT secret key
- CORS origins
- Token expiration time

### Frontend Configuration
- API base URL
- Next.js configuration
- Tailwind CSS customization

## Development

### Backend Development
- Use FastAPI's automatic API documentation at `/docs`
- Implement new endpoints in `app/routers/`
- Add business logic in `app/services/`
- Update models in `app/models.py`

### Frontend Development
- Components in `components/`
- Pages in `app/`
- API calls in `lib/api.ts`
- Styling with Tailwind CSS

## Testing

### Backend Testing
```bash
cd backend
pytest
```

### Frontend Testing
```bash
cd frontend
npm run test
```

## Deployment

### Backend Deployment
1. Set production environment variables
2. Use production database (PostgreSQL recommended)
3. Deploy with Gunicorn or similar WSGI server
4. Set up reverse proxy (Nginx)

### Frontend Deployment
1. Build the application: `npm run build`
2. Deploy to Vercel, Netlify, or similar platforms
3. Configure environment variables
4. Update API base URL for production

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please open an issue in the GitHub repository.

## Roadmap

- [ ] Advanced conflict resolution
- [ ] Multi-school support
- [ ] Mobile app
- [ ] Advanced analytics
- [ ] Integration with school management systems
- [ ] Real-time updates
- [ ] Advanced export formats (PDF, Excel)
- [ ] Teacher availability management
- [ ] Room allocation system
