# In The Picture

**A simple image upload and gallery application built with Python Flask**

Used as the hands-on exercise application for the GitHub Fundamentals training course at AT Computing.

---

## 📸 Overview

"In The Picture" is a lightweight web application that allows users to:
- Upload images through a web interface
- View uploaded images in a gallery format
- Preview individual images
- Download images
- Delete images (feature added in Exercise 03)

The application demonstrates a simplified web stack:
- **Frontend**: HTML templates with Bootstrap CSS
- **Backend**: Python Flask web framework
- **Storage**: Filesystem storage (no database required)
- **Deployment**: Single Docker container

**Key Features**:
- ✅ Single container architecture (no dependencies)
- ✅ Filesystem-based storage (no database setup)
- ✅ Simple deployment (`./docker-run.sh`)
- ✅ Perfect for learning Git/GitHub workflows

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│  Web Browser (http://localhost:5001)   │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│       Flask Application (Python)        │
│  - Routes (/, /upload, /delete, etc.)   │
│  - Template rendering (Jinja2)          │
│  - File handling                        │
└──────────────────┬──────────────────────┘
                   │
                   ▼
            ┌──────────────┐
            │  Filesystem  │
            │  (/pictures) │
            │              │
            │ *.jpg, *.png │
            └──────────────┘
```

**Design Philosophy**: Keep it simple! No database means:
- Faster startup (seconds, not minutes)
- Fewer moving parts (one container vs. two)
- Easier troubleshooting (no connection issues)
- Perfect for CI/CD learning (quick builds)

---

## 🛠️ Tech Stack

| Component | Technology | Version |
|-----------|------------|---------|
| Language | Python | 3.10.12 |
| Web Framework | Flask | 3.0.0 |
| Container Runtime | Docker | 20.10+ |
| Frontend | Bootstrap CSS | 5.x |
| Icons | BoxIcons | 2.1.4 |
| Testing | pytest | 7.4.3 |
| Linting | flake8 | 6.1.0 |

---

## 📁 Project Structure

```
app/
├── docker-run.sh               # Build and run script (replaces docker-compose)
├── Dockerfile                  # Container build instructions
├── .gitignore                  # Git ignore patterns
├── README.md                   # This file
├── files/
│   ├── app/
│   │   ├── app.py              # Main Flask application
│   │   ├── templates/          # Jinja2 HTML templates
│   │   │   ├── base.html       # Base layout template
│   │   │   ├── index.html      # Upload form + gallery
│   │   │   ├── preview.html    # Individual image preview
│   │   │   └── message.html    # Status messages
│   │   └── static/             # CSS, JavaScript, images
│   │       ├── bootstrap.min.css
│   │       ├── bootstrap.bundle.min.js
│   │       ├── AT-LOGO-WEB-BL-v1.png
│   │       └── inthepicture.png
│   ├── requirements.txt        # Python dependencies
│   ├── pytest.ini              # Pytest configuration
│   ├── .flake8                 # Linting configuration
│   └── tests/                  # Test suite
│       ├── test_app.py         # Application tests
│       └── conftest.py         # Pytest fixtures
└── [deprecated files kept for reference]
    ├── docker-compose.yml      # Old orchestration (no longer used)
    ├── .env.example            # Old environment vars (no longer needed)
    └── inthepicture.sql        # Old database schema (no longer needed)
```

**Note**: Images are stored in `/pictures` directory inside the container (mapped to `uploads/` on host if you mount it).

---

## 🚀 Quick Start

### Prerequisites

- **Docker** (20.10+): [Install Docker](https://docs.docker.com/get-docker/)

**Verify installation:**
```bash
docker --version
```

### Step 1: Navigate to App Directory

```bash
cd app/
```

### Step 2: Build and Run

```bash
./docker-run.sh
```

**What this does:**
1. Builds the Flask application Docker image
2. Stops and removes any existing container
3. Starts new container on port 5001
4. Creates `/pictures` directory for image storage

**Wait ~5 seconds** for container to fully start.

### Step 3: Access the Application

Open your web browser and navigate to:

```
http://localhost:5001
```

**You should see:**
- "IN THE PICTURE" header
- File upload form
- Empty gallery (no images yet)

### Step 4: Upload an Image

1. Click **Choose File**
2. Select an image from your computer (.jpg, .png, .gif, .svg)
3. Click **Upload**
4. Image should appear in the gallery below

### Step 5: Stop the Application (When Done)

```bash
./docker-run.sh --stop
```

**What this does:**
- Stops the container
- Removes the container
- **Note**: Images are stored inside the container, so they'll be lost when container is removed

---

## 🔄 Common Operations

### View Application Logs

```bash
# View logs
docker logs inthepicture-app

# Follow logs in real-time
docker logs -f inthepicture-app
```

### Restart Application

```bash
# Stop current container
./docker-run.sh --stop

# Start new container
./docker-run.sh
```

### Rebuild After Code Changes

```bash
# Stop and rebuild
./docker-run.sh --stop
./docker-run.sh

# The script automatically rebuilds the image
```

### Access Container Shell

```bash
docker exec -it inthepicture-app bash
```

**Useful for debugging:**
```bash
# Inside container
ls -la /pictures/           # View uploaded images
cat /app/app.py            # View application code
env | grep PICTURES_DIR    # Check environment variables
```

### Persist Images Between Restarts

By default, images are stored inside the container and lost on restart. To persist them:

```bash
# Run with volume mount
docker run -d \
    --name inthepicture-app \
    -p 5001:5001 \
    -v $(pwd)/uploads:/pictures \
    inthepicture:latest
```

---

## 🧪 Development

### Running Locally (Without Docker)

**Prerequisites:**
- Python 3.10+
- pip

**Steps:**

```bash
# Navigate to files directory
cd files/

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variable (optional, defaults to 'uploads')
export PICTURES_DIR=uploads

# Create uploads directory
mkdir -p uploads

# Run application
python app/app.py
```

**Access at**: `http://localhost:5001`

**Stop**: Press `Ctrl+C`

### Running Tests

```bash
# Navigate to files directory
cd files/

# Run pytest
pytest

# Run with coverage
pytest --cov=app --cov-report=term-missing

# Run with verbose output
pytest -v
```

**Expected output:**
```
============================= test session starts ==============================
collected 5 items

tests/test_app.py::test_home_page PASSED                                 [ 20%]
tests/test_app.py::test_upload_page_exists PASSED                        [ 40%]
tests/test_app.py::test_file_upload PASSED                               [ 60%]
tests/test_app.py::test_static_route PASSED                              [ 80%]
tests/test_app.py::test_preview_route PASSED                             [100%]

============================== 5 passed in 0.23s ===============================
```

### Running Linter

```bash
# Navigate to files directory
cd files/

# Run flake8
flake8 app/

# Check specific file
flake8 app/app.py
```

---

## 🛣️ Application Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Homepage: upload form + image gallery |
| `/upload` | POST | Handle file upload |
| `/preview/<imgname>` | GET | Preview individual image |
| `/download/<imgname>` | GET | Download image file |
| `/delete/<imgname>` | POST | Delete image (added in Exercise 03) |
| `/static/<name>` | GET | Serve static files (CSS, JS, images) |

---

## 🔒 Security Considerations

### Current Security Issues (Educational Context)

This application is designed for **local training exercises only** and has several security issues:

1. **No Authentication**: Anyone can upload/delete (should require login)
2. **No File Size Limits**: Could fill disk with large uploads
3. **Basic Input Validation**: Relies on client-side file type checking
4. **No HTTPS**: Traffic is unencrypted (use reverse proxy in production)
5. **No Rate Limiting**: Vulnerable to abuse
6. **Ephemeral Storage**: Images lost when container restarts (by design for training)

### What's Done Right

- ✅ **`secure_filename()`** usage (prevents path traversal)
- ✅ **File type validation** (checks extensions)
- ✅ **Error handling** (graceful failures)
- ✅ **Simple architecture** (fewer attack surfaces than database version)

### For Production Use

If deploying this for real use (not recommended), you would need:

1. **User authentication** (Flask-Login or OAuth)
2. **File upload limits** in Flask config
3. **Server-side file type validation** (check magic bytes, not just extension)
4. **HTTPS** with valid certificate
5. **Rate limiting** on upload endpoint
6. **CSRF protection** (Flask-WTF)
7. **Use production WSGI server** (Gunicorn, not Flask dev server)
8. **Persistent storage** (volume mounts or object storage)
9. **Regular security updates** for dependencies
10. **Content Security Policy** headers

**💡 Teaching moment**: This app demonstrates why security is hard. Even a simple upload form has many attack vectors!

---

## 🐛 Troubleshooting

### Port Already in Use

**Error**: `Bind for 0.0.0.0:5001 failed: port is already allocated`

**Solution**:
```bash
# Option 1: Stop process using port 5001
# Find process
lsof -i :5001  # macOS/Linux
netstat -ano | findstr :5001  # Windows

# Kill process
kill -9 <PID>

# Option 2: Change port in docker-run.sh
# Edit script to use different port:
PORT="8080"
```

### Container Won't Start

**Check logs:**
```bash
docker logs inthepicture-app
```

**Common issues:**
- **Docker daemon not running** → Start Docker Desktop
- **Insufficient disk space** → Free up space or prune: `docker system prune`
- **Previous container still running** → `./docker-run.sh --stop` first
- **Port conflict** → See "Port Already in Use" above

### Images Upload But Don't Appear

**Possible causes:**
1. **File permissions** - Container can't write to /pictures
2. **Browser cache** - Hard refresh: `Ctrl+Shift+R` (Windows/Linux) or `Cmd+Shift+R` (macOS)
3. **Upload failed** - Check container logs for errors

**Debug:**
```bash
# Check if image in container
docker exec inthepicture-app ls -la /pictures/

# Check container logs
docker logs inthepicture-app

# Check file was uploaded (look for "File uploaded: filename")
docker logs inthepicture-app | grep "uploaded"
```

### Docker Command Not Found

**Error**: `docker: command not found`

**Solution**: Install Docker Desktop
- **macOS/Windows**: [Docker Desktop](https://www.docker.com/products/docker-desktop)
- **Linux**: [Docker Engine](https://docs.docker.com/engine/install/)

**Verify installation:**
```bash
docker --version
docker ps
```

### Permission Denied When Running docker-run.sh

**Error**: `Permission denied: ./docker-run.sh`

**Solution**: Make script executable
```bash
chmod +x docker-run.sh
./docker-run.sh
```

---

## 🎓 Learning Resources

### Flask Documentation
- [Flask Quickstart](https://flask.palletsprojects.com/quickstart/)
- [Flask Templates](https://flask.palletsprojects.com/templates/)
- [Flask Security](https://flask.palletsprojects.com/security/)

### Docker Documentation
- [Docker Get Started](https://docs.docker.com/get-started/)
- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
- [Docker CLI Reference](https://docs.docker.com/engine/reference/commandline/cli/)

### Python Testing
- [pytest Documentation](https://docs.pytest.org/)
- [flake8 Documentation](https://flake8.pycqa.org/)

---

## 📝 Exercise Modifications

Throughout the GitHub Fundamentals course, you'll modify this application:

| Exercise | Modification | Skills Practiced |
|----------|--------------|------------------|
| 02 | Clone and run locally | Git clone, SSH, Docker basics |
| 03 | Add delete image feature | Branching, PRs, code changes |
| 04 | Create intentional conflicts | Merge conflict resolution |
| 05 | Add CI/CD pipeline | GitHub Actions, pytest, Docker build, ACR push |
| 06 | Configure ACR secrets | Secrets management, registry auth |
| 07 | Enable branch protection | Professional workflows |

---

## 🚢 CI/CD Integration

This application includes a complete CI/CD pipeline (added in Exercise 05):

**Pipeline Steps**:
1. **Lint** - flake8 code quality checks
2. **Test** - pytest unit tests
3. **Build** - Docker image build
4. **Push** - Publish to Azure Container Registry

**Workflow file**: `.github/workflows/ci.yml`

**Image Tags**:
- `latest` - Most recent successful build
- `<commit-sha>` - Specific commit version

**Pull image from ACR** (after Exercise 06):
```bash
# Login to ACR (use credentials from trainer)
echo "$ACR_PASSWORD" | docker login $ACR_REGISTRY_URL \
  --username $ACR_USERNAME \
  --password-stdin

# Pull image
docker pull $ACR_REGISTRY_URL/inthepicture:latest

# Run image
docker run -d \
  --name inthepicture-app \
  -p 5001:5001 \
  $ACR_REGISTRY_URL/inthepicture:latest
```

---

## 🤝 Contributing

This is a training application maintained by AT Computing. If you find bugs or have suggestions:

1. Create an Issue describing the problem
2. Fork the repository
3. Create a feature branch
4. Make your changes
5. Open a Pull Request

**For students**: Practice the PR workflow! Your contributions help improve the course for future students.

---

## 📄 License

Copyright © 2026 AT Computing

This application is provided for educational purposes as part of the GitHub Fundamentals training course.

---

## ✨ Credits

- **AT Computing** training development team
- **Bootstrap** for responsive CSS framework
- **BoxIcons** for icon library
- **Flask** open source community

---

**Happy Learning!** 🎓

Need help? Refer to the exercise troubleshooting sections or ask your instructor.
