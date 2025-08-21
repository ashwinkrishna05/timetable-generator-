# Project Structure

```
school-timetable-generator/
├── README.md                 # Main project documentation
├── PROJECT_STRUCTURE.md      # This file - project structure overview
├── enhanced_timetable_generator_complete.py  # Original Python application
│
├── backend/                  # Python FastAPI Backend
│   ├── requirements.txt      # Python dependencies
│   ├── main.py              # FastAPI application entry point
│   ├── start.py             # Startup script
│   ├── .env                 # Environment variables (create this)
│   │
│   ├── app/                 # Main application package
│   │   ├── __init__.py
│   │   ├── config.py        # Configuration settings
│   │   ├── database.py      # Database connection and session
│   │   ├── models.py        # SQLAlchemy database models
│   │   ├── schemas.py       # Pydantic request/response schemas
│   │   │
│   │   ├── routers/         # API route handlers
│   │   │   ├── __init__.py
│   │   │   ├── auth.py      # Authentication endpoints
│   │   │   ├── schools.py   # School management endpoints
│   │   │   ├── classes.py   # Class management endpoints
│   │   │   ├── subjects.py  # Subject management endpoints
│   │   │   ├── teachers.py  # Teacher management endpoints
│   │   │   └── timetables.py # Timetable generation endpoints
│   │   │
│   │   └── services/        # Business logic services
│   │       ├── __init__.py
│   │       └── timetable_service.py  # Core timetable generation logic
│   │
│   └── timetable_generator.db  # SQLite database (auto-generated)
│
└── frontend/                 # Next.js Frontend
    ├── package.json          # Node.js dependencies
    ├── next.config.js        # Next.js configuration
    ├── tailwind.config.js    # Tailwind CSS configuration
    ├── start.sh              # Startup script (Unix/Mac)
    │
    ├── app/                  # Next.js 14 app directory
    │   ├── layout.tsx        # Root layout component
    │   ├── page.tsx          # Main dashboard page
    │   ├── globals.css       # Global styles
    │   ├── providers.tsx     # React Query provider
    │   │
    │   ├── schools/          # School management pages
    │   ├── classes/          # Class management pages
    │   ├── teachers/         # Teacher management pages
    │   ├── timetables/       # Timetable pages
    │   └── auth/             # Authentication pages
    │
    ├── components/           # Reusable UI components
    │   ├── DashboardCard.tsx # Dashboard statistics card
    │   ├── ui/               # Base UI components
    │   │   └── Button.tsx    # Button component
    │   └── forms/            # Form components
    │
    ├── lib/                  # Utility libraries
    │   └── api.ts            # API client configuration
    │
    └── types/                # TypeScript type definitions
        └── index.ts          # Global type definitions
```

## Key Components

### Backend (Python/FastAPI)

1. **Models** (`app/models.py`): Database entities using SQLAlchemy
   - School, Class, Subject, Teacher, Timetable, ECA, Lab, User

2. **Schemas** (`app/schemas.py`): Pydantic models for API validation
   - Request/response models with proper validation

3. **Routers** (`app/routers/`): API endpoint handlers
   - RESTful CRUD operations for all entities
   - Authentication and authorization

4. **Services** (`app/services/`): Business logic
   - Timetable generation algorithm
   - Teacher workload calculation
   - Substitute teacher finding

5. **Database** (`app/database.py`): Database configuration
   - SQLAlchemy setup with SQLite/PostgreSQL support

### Frontend (Next.js/React)

1. **Pages** (`app/`): Application pages using Next.js 14 app router
   - Dashboard, CRUD operations, timetables

2. **Components** (`components/`): Reusable UI components
   - Dashboard cards, forms, buttons, tables

3. **API Client** (`lib/api.ts`): HTTP client configuration
   - Axios setup with interceptors
   - Authentication token management

4. **Styling** (`globals.css`, `tailwind.config.js`): CSS framework
   - Tailwind CSS with custom components

## Data Flow

1. **User Input** → Frontend forms
2. **API Calls** → Backend endpoints
3. **Business Logic** → Service layer
4. **Database** → SQLAlchemy models
5. **Response** → Frontend display

## Development Workflow

1. **Backend Development**:
   - Add models in `app/models.py`
   - Create schemas in `app/schemas.py`
   - Implement business logic in `app/services/`
   - Add API endpoints in `app/routers/`

2. **Frontend Development**:
   - Create pages in `app/`
   - Build components in `components/`
   - Add API calls in `lib/api.ts`
   - Style with Tailwind CSS

3. **Testing**:
   - Backend: Use FastAPI's built-in testing
   - Frontend: React Testing Library
   - API: Postman or similar tools

## Deployment

- **Backend**: Deploy to cloud platforms (Heroku, AWS, etc.)
- **Frontend**: Deploy to Vercel, Netlify, or similar
- **Database**: Use PostgreSQL for production
- **Environment**: Set production environment variables

## Security Features

- JWT-based authentication
- Password hashing with bcrypt
- CORS configuration
- Input validation with Pydantic
- SQL injection protection with SQLAlchemy
