## Football League Manager 
The Football League Manager is a modern web-based application developed using Django and Bootstrap that allows users to create, organize, and manage football leagues with an automated Premier League-style points system. The system is designed to simplify league administration by enabling users to register accounts, create custom leagues, add teams, generate fixtures automatically, enter match results, and view live standings in real time.

The application uses a round-robin fixture generation algorithm to create fair home-and-away matches for all teams in a league. Once match results are entered, the platform automatically calculates team statistics including matches played, wins, draws, losses, goals scored, goals conceded, goal difference, and total points. League tables are dynamically updated and sorted according to official football ranking rules: Points → Goal Difference → Goals Scored.

The project includes a secure authentication system where users can register, log in, and manage only their own leagues. Each league contains dedicated sections for teams, fixtures, and standings, all presented through a responsive and user-friendly interface styled with Bootstrap. The system also supports fixture regeneration, result editing, and league deletion.

Additionally, the application is deployment-ready with support for tools such as GitHub, Railway, and Render, making it suitable for both academic and real-world use. Static file management is handled using WhiteNoise, while environment variables are securely managed using python-decouple.

### Key Features

* User registration and authentication
* Create and manage multiple football leagues
* Add and remove teams
* Automatic home-and-away fixture generation
* Live Premier League-style standings table
* Match result entry and editing
* Goal difference and points calculations
* Responsive Bootstrap user interface
* Admin panel support through Django Admin
* Deployment-ready configuration

### Technologies Used

* Python
* Django
* Bootstrap 5
* SQLite
* WhiteNoise
* Gunicorn
* HTML/CSS
* Git & GitHub

### Purpose of the Project

The project is designed to help football organizers, schools, communities, or sports enthusiasts efficiently manage football competitions digitally instead of relying on manual calculations and paper records. It also serves as an educational full-stack web development project demonstrating backend logic, database management, authentication systems, and responsive frontend design using Django.
