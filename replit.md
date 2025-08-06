# Overview

This is a liver disease prediction application that uses AI-powered medical assessment to evaluate liver health risk factors. The application provides a comprehensive health questionnaire interface where users can input medical data and receive risk assessments with personalized recommendations. It's designed as a clinical screening tool to assist healthcare professionals in preliminary liver disease risk evaluation.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Framework**: React with TypeScript, built using Vite for fast development and builds
- **UI Library**: Shadcn/ui components built on Radix UI primitives for accessibility and consistency
- **Styling**: Tailwind CSS with custom medical theme colors and CSS variables for design system consistency
- **State Management**: React Hook Form for form handling with Zod validation, TanStack Query for server state management
- **Routing**: Wouter for lightweight client-side routing

## Backend Architecture
- **Framework**: Express.js with TypeScript for RESTful API endpoints
- **ML Integration**: Python FastAPI service integration for real-time machine learning predictions
- **Prediction Engine**: Integrated ML model serving with automatic feature preprocessing and standard scaling
- **API Design**: RESTful endpoints for prediction submission (/api/predict) and history retrieval (/api/predictions)
- **Data Validation**: Zod schemas for request/response validation with strict medical parameter constraints
- **Error Handling**: Comprehensive error handling with ML service availability checking and detailed user feedback

## Data Storage Solutions
- **Database**: PostgreSQL configured via Drizzle ORM for type-safe database operations
- **Schema Management**: Drizzle Kit for database migrations and schema evolution
- **Connection**: Neon Database serverless PostgreSQL for cloud-native scalability
- **Fallback Storage**: In-memory storage implementation for development and testing scenarios

## Development Architecture
- **Monorepo Structure**: Shared schema definitions between client and server in /shared directory
- **Build System**: Vite for frontend bundling, ESBuild for server bundling with external package handling
- **Development Server**: Hot reload with Vite middleware integration and development banner for Replit environment
- **Type Safety**: Strict TypeScript configuration with path mapping for clean imports

## ML Integration Architecture
- **Python ML Service**: FastAPI-based microservice serving trained pickle models on port 8001
- **Feature Processing**: Automatic conversion from form data to model-ready features with categorical encoding
- **Data Preprocessing**: Standard scaler integration for proper feature normalization
- **Model Requirements**: Supports both trained model (.pkl) and standard scaler (.pkl) files
- **Error Handling**: Graceful error messages when ML service or model files are unavailable
- **Service Communication**: Node.js backend communicates with Python ML service via HTTP API calls

## ML Service Setup
- **Model Files**: Place trained model in `ml_service/liver_disease_model.pkl`
- **Scaler Files**: Place standard scaler in `ml_service/standard_scaler.pkl`
- **Service Start**: Run `python3 start_ml_service.py` to start ML service on port 8001
- **Integration Test**: Use `python3 test_ml_integration.py` to verify setup
- **Feature Format**: 10 features including age, gender, BMI, lifestyle factors, and medical history

# External Dependencies

## Database Services
- **Neon Database**: Serverless PostgreSQL hosting with connection pooling and automatic scaling
- **Drizzle ORM**: Type-safe database operations with PostgreSQL dialect support

## UI and Component Libraries
- **Radix UI**: Comprehensive set of accessible, unstyled UI primitives for form controls, dialogs, and interactive elements
- **Shadcn/ui**: Pre-built component library with consistent design system and Tailwind integration
- **Lucide React**: Medical and general-purpose icons for intuitive user interface elements

## Form and Validation
- **React Hook Form**: Performance-optimized form handling with minimal re-renders
- **Zod**: Runtime type validation for medical data with comprehensive error messaging
- **Hookform Resolvers**: Integration layer between React Hook Form and Zod validation

## Development and Build Tools
- **Vite**: Fast development server and build tool with React plugin support
- **TanStack Query**: Server state management for API calls with caching and background updates
- **Date-fns**: Date manipulation utilities for timestamp handling and formatting
- **Replit Integration**: Development environment plugins for error overlay and cartographer mapping

## ML and Python Services
- **FastAPI**: Python web framework for serving machine learning models
- **NumPy**: Numerical computing for feature preprocessing and model operations
- **Joblib**: Model persistence and loading for pickle files
- **Scikit-learn**: Machine learning utilities and standard scaler functionality
- **Uvicorn**: ASGI server for running the FastAPI ML service

## Styling and Design
- **Tailwind CSS**: Utility-first CSS framework with custom medical theme configuration
- **Class Variance Authority**: Type-safe variant handling for component styling
- **Embla Carousel**: Touch-friendly carousel component for result presentation