# sql-database-project
A database project to help users find stores nearby offering discounts on products they need, simplifying shopping and saving money.

Project Overview
This is a database project to help users find stores and product discounts. We will be using SQL for database management to demonstrate an efficient way of searching for deals and stores from the database tables, alongside a user-friendly interface using web tech.

Features
- Locate stores with active discounts and promotions
- Search by product, store location, or deal category
- Effective querying to demonstrate the use of SQL and database skills.
- User interface to interact with the database and show results

  Tech Stack
  Database: MySQL workbench
  Backend: Node.js, Python
  Frontend: React(javascript), HTML, CSS
  Tools: GitHub



## TO RUN Project:
## On vs code studio preffered IDE,
Make sure you have clone the repository and created your own branches.
git checkout -b <branch-name> --Replace <branch-name> with a name your name or task you're working on
git push origin <branch-name> --Push the branch to the remote repository so others can see it


Now, we will set up your environment to match mines so the project works on your machines. 

  ## Environment Setup

1. Create a `.env` file in the root of your project directory.
2. Copy the content from `.env.example` and replace `your_secret_key_here` with your own generated secret key.
3. rename it to .env, then update the values of Db credentials with your specific configuration.
4.  Navigate to the Backend Directory: cd backend
5.  Create a Virtual Environment: python -m venv venv
6.  Activate the Virtual Environment: .\venv\Scripts\Activate
7.  Once the virtual environment is activated, install all the necessary dependencies(contained in requirements.txt) by running
    pip install -r requirements.txt

8. Finally cd to backend folder level and run python app.py to start webpage


Disclaimer
Some basic form inputs and template layouts in this project were created with the help of OpenAI's GPT to focus on core functionality like database management and backend logic. All content was reviewed and tailored to project needs.