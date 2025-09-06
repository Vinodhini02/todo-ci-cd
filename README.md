Todo Flask App - GitHub Repo
Project Description:
A simple Todo web application built with Flask, Dockerized, and ready for CI/CD.
Features:
- Add, update, delete, and view tasks
- REST API endpoints
- Dockerized for easy deployment
- Automated testing with Pytest
Tech Stack:
- Python & Flask
- Docker
- Pytest
- CI/CD with GitHub Actions
Setup & Run:
1. Clone Repo:
 git clone https://github.com/Vinodhini02/todo-ci-cd.git
 cd todo-ci-cd
2. Create Virtual Environment:
 python -m venv .venv
 # Linux / Mac
 source .venv/bin/activate
 # Windows PowerShell
 .venv\Scripts\Activate.ps1
3. Install Dependencies:
 pip install -r requirements.txt
4. Run Tests:
 pytest -q
5. Start App:
 python app.py
 Open http://localhost:8000
Docker:
- Build Image:
 docker build -t todo-flask .
- Run Container:
 docker run -p 8000:8000 todo-flask
Contributing:
1. Fork the repo
2. Create a branch: git checkout -b feature/your-feature
3. Commit changes: git commit -m "Add feature"
4. Push branch: git push origin feature/your-feature
5. Open a Pull Request
