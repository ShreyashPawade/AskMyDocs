# AskMyDocs Frontend - Project Structure

## 📁 Complete File Manifest

### Core Application Files

```
frontend/
│
├── streamlit_app.py              # Main application entry point
│   └── Initializes session, loads CSS, renders header and chat
│
├── api.py                        # Backend API client
│   └── Centralized API communication with error handling
│
├── config.py                     # Configuration and constants
│   └── API endpoints, theme colors, UI settings
│
├── style.css                     # Custom CSS styling
│   └── Dark professional theme, responsive design
```

### Component Modules

```
components/
├── __init__.py                   # Package initialization
│
├── header.py                     # App header component
│   └── Displays title, subtitle, backend status indicator
│
├── sidebar.py                    # Sidebar container
│   └── Organizes upload and documents sections
│
├── upload.py                     # PDF upload component
│   └── File upload, validation, backend integration
│
├── documents.py                  # Document management
│   └── Document list, details view, delete functionality
│
├── chat.py                       # Main chat interface
│   └── Message display, chat input, response handling
│
├── confidence.py                 # Confidence badge component
│   └── Color-coded confidence visualization
│
└── sources.py                    # Citation sources component
    └── Document source display with page numbers
```

### Utility Modules

```
utils/
├── __init__.py                   # Package initialization
│
├── session.py                    # Session state management
│   └── Session ID, message history, backend status
│
└── helpers.py                    # Helper functions
    └── Logging, formatting, text processing utilities
```

### Configuration Files

```
.streamlit/
└── config.toml                   # Streamlit configuration
    └── Theme, server settings, logging

.env.example                      # Environment template
└── Configuration for backend URL and Streamlit

.gitignore                        # Git ignore rules
└── Excludes cache, venv, secrets

.streamlit/config.toml            # Streamlit config
└── Theme colors, server ports, UI settings
```

### Setup and Deployment

```
setup.sh                          # Linux/macOS setup script
└── Automated environment setup and dependency installation

setup.bat                         # Windows setup script
└── Automated setup for Windows systems

requirements.txt                  # Python dependencies
└── Streamlit, Requests, python-dotenv

Dockerfile                        # Docker container definition
└── Multi-stage build for production deployment

docker-compose.yml                # Docker Compose configuration
└── Frontend + backend orchestration
```

### Documentation

```
README.md                         # Main documentation
├── Features overview
├── Installation guide
├── Usage instructions
├── Configuration guide
├── Deployment options
└── Troubleshooting

QUICKSTART.md                     # Quick start guide
├── 5-minute setup
├── Common tasks
├── Troubleshooting quick fixes
└── Learning resources

DEVELOPMENT.md                    # Developer guide
├── Architecture overview
├── Development workflow
├── Code style guide
├── Testing guidance
├── Performance optimization
└── Common patterns

API.md                           # API integration guide
├── All endpoints documented
├── Request/response examples
├── Error handling
├── Session management
└── Testing guide
```

## 📊 File Statistics

### Python Files
- **streamlit_app.py**: 54 lines (main app)
- **api.py**: 270 lines (API client)
- **config.py**: 150 lines (configuration)
- **components/header.py**: 35 lines
- **components/sidebar.py**: 22 lines
- **components/chat.py**: 280 lines
- **components/upload.py**: 55 lines
- **components/documents.py**: 110 lines
- **components/confidence.py**: 35 lines
- **components/sources.py**: 45 lines
- **utils/session.py**: 250 lines
- **utils/helpers.py**: 240 lines

**Total Python Code**: ~1,350 lines

### CSS Styling
- **style.css**: 600+ lines of custom styling

### Documentation
- **README.md**: ~500 lines
- **QUICKSTART.md**: ~300 lines
- **DEVELOPMENT.md**: ~600 lines
- **API.md**: ~700 lines

## 🎯 File Dependencies

```
streamlit_app.py
├── config.py
├── components/header.py
│   ├── api.py
│   └── utils/session.py
├── components/sidebar.py
│   ├── components/upload.py
│   │   ├── api.py
│   │   └── utils/session.py
│   └── components/documents.py
│       ├── api.py
│       └── utils/session.py
└── components/chat.py
    ├── api.py
    ├── components/confidence.py
    ├── components/sources.py
    └── utils/session.py

api.py
└── config.py
    └── utils/helpers.py

utils/session.py
└── config.py
    └── utils/helpers.py
```

## 📦 Dependencies

### Required Packages
```
streamlit==1.32.2          # Web framework
requests==2.31.0          # HTTP client
python-dotenv==1.0.0      # Environment configuration
```

### Development Tools (Optional)
```
pytest==7.4.0              # Testing framework
pytest-cov==4.1.0          # Coverage reporting
pylint==2.17.0             # Code analysis
black==23.7.0              # Code formatting
isort==5.12.0              # Import sorting
```

## 🔧 Configuration Hierarchy

```
Environment Variables (.env)
├── BACKEND_URL (highest priority)
└── Streamlit settings

Config File (.streamlit/config.toml)
├── Theme settings
└── Server settings

config.py (Constants)
├── API endpoints
├── Theme colors
├── UI constants
└── Default values

Hardcoded values (Lowest priority)
└── Fallback defaults
```

## 📂 Directory Permissions

```
frontend/
├── streamlit_app.py         [rw] Read/Write
├── components/              [rwx] Directory
│   └── *.py                [rw] Read/Write
├── utils/                   [rwx] Directory
│   └── *.py                [rw] Read/Write
├── .streamlit/              [rwx] Directory
│   └── config.toml         [rw] Read/Write
├── .env                     [rw] Read/Write (secret)
├── style.css                [r]  Read-only (CSS)
└── requirements.txt         [r]  Read-only (dependencies)
```

## 🚀 Runtime Files Generated

During execution, Streamlit creates:

```
.streamlit/
├── secrets.toml            (created if needed)
└── logs/
    └── 2024-*.log         (log files)

__pycache__/               (Python cache)
├── streamlit_app.cpython-*.pyc
└── ...other .pyc files

.pytest_cache/             (if running tests)

venv/                      (virtual environment)
├── lib/
├── bin/
└── include/
```

These are automatically generated and listed in `.gitignore`.

## 🔐 Sensitive Files

Files that should NEVER be committed:

```
.env                       # Environment secrets
.env.local                 # Local overrides
.streamlit/secrets.toml    # Streamlit secrets
venv/                      # Virtual environment
__pycache__/               # Python cache
.pytest_cache/             # Test cache
*.log                      # Log files
.vscode/settings.json      # IDE settings with secrets
```

## 📝 File Descriptions

### Core Application

**streamlit_app.py**
- Main entry point for the Streamlit app
- Configures page settings
- Loads custom CSS
- Renders header and chat interface

**api.py**
- Centralized API client for backend communication
- Handles all HTTP requests with error handling
- Implements timeout and retry logic
- Validates responses

**config.py**
- Centralized configuration management
- API endpoints
- Theme colors (all CSS variables)
- UI constants and display strings
- Upload constraints

**style.css**
- Professional dark theme styling
- CSS variables for consistency
- Responsive design utilities
- Animation definitions
- Component-specific styles

### Components

**header.py**
- Renders app title and subtitle
- Shows backend status indicator
- Implements status pulsing animation

**sidebar.py**
- Container for sidebar sections
- Organizes upload and documents components

**upload.py**
- File upload widget
- File validation
- Upload progress indication
- Success/error handling

**documents.py**
- Document list display
- Document cards with metadata
- Delete confirmation
- Details view modal

**chat.py**
- Message display area
- Chat input field
- Message formatting
- Response streaming preparation

**confidence.py**
- Color-coded confidence badge
- Animated indicator dot
- Confidence level calculation

**sources.py**
- Expandable sources section
- Source item cards
- Page and chunk reference display

### Utilities

**session.py**
- Session state initialization
- Message history management
- Backend status tracking
- Document list management
- Session ID generation and validation

**helpers.py**
- Text formatting and truncation
- Confidence level calculation
- Timestamp formatting
- File extension validation
- JSON extraction from responses

### Configuration & Deployment

**.streamlit/config.toml**
- Streamlit theme configuration
- Server settings
- Client-side behavior
- Logger configuration

**.env.example**
- Template for environment variables
- Documents required configuration
- Instructions for customization

**.gitignore**
- Python cache exclusions
- Virtual environment exclusions
- IDE settings exclusions
- Log file exclusions
- Secret file exclusions

**setup.sh / setup.bat**
- Automated environment setup
- Virtual environment creation
- Dependency installation
- Configuration file creation

**requirements.txt**
- Python package dependencies
- Pinned versions for reproducibility

**Dockerfile**
- Multi-stage production build
- Health checks
- Configuration file generation

**docker-compose.yml**
- Frontend service definition
- Backend service definition
- Network configuration
- Volume mounts

### Documentation

**README.md**
- Project overview
- Feature list
- Installation instructions
- Usage guide
- Troubleshooting
- Deployment guide

**QUICKSTART.md**
- Fast setup instructions
- Common task guides
- Quick troubleshooting

**DEVELOPMENT.md**
- Architecture overview
- Development workflow
- Code style guide
- Testing guide
- Performance optimization

**API.md**
- Complete API reference
- Request/response examples
- Error handling guide
- Session management
- Testing instructions

## 🎓 Learning Path

1. **First Time?**
   - Read QUICKSTART.md
   - Run setup script
   - Upload a document
   - Ask a question

2. **Want to Use It?**
   - Read README.md
   - Review configuration options
   - Deploy with Docker or manual setup

3. **Want to Develop?**
   - Read DEVELOPMENT.md
   - Review architecture
   - Follow coding standards
   - Write tests

4. **Need API Details?**
   - Check API.md
   - Review api.py
   - Test endpoints with curl

## 📈 Code Quality Metrics

- **Code Coverage**: Not yet configured (TBD)
- **Type Hints**: Used in utilities (60% coverage)
- **Docstrings**: All functions documented
- **Style**: PEP8 compliant
- **Security**: No hardcoded secrets

## 🔄 Version Control

### Commits Structure
```
frontend/
├── .gitignore              # All secrets/cache excluded
├── .git/                   # Git history
└── ...                     # Tracked files
```

### Recommended Commit Messages
```
feat: Add streaming support to chat
fix: Handle connection errors gracefully
docs: Update API documentation
style: Format CSS variables
test: Add session management tests
refactor: Modularize chat component
```

## 📱 Responsive Breakpoints

CSS media queries for:
- Desktop: 1024px+
- Tablet: 768px - 1024px
- Mobile: < 768px

## 🎨 Color Palette

All colors defined as CSS variables in `style.css`:

| Variable | Color | Use |
|----------|-------|-----|
| --primary | #6366F1 | Indigo accent |
| --success | #10B981 | Green feedback |
| --warning | #F59E0B | Amber caution |
| --danger | #EF4444 | Red error |

See style.css for complete palette.

---

**Total Project Size**: ~2,500 lines of code + 2,000 lines of documentation

**Last Updated**: 2024
