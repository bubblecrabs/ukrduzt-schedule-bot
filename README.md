# Telegram Bot for University Schedule (UkrDUZT)
[![Python](https://img.shields.io/badge/Python-3.12-green)](https://www.python.org/)
[![Aiogram](https://img.shields.io/badge/Aiogram-3.17.0-blue)](https://docs.aiogram.dev/)
[![Aiohttp](https://img.shields.io/badge/Aiohttp-3.11+-blue)](https://docs.aiohttp.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-2.10+-red)](https://docs.pydantic.dev/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red)](https://www.sqlalchemy.org/)
[![Alembic](https://img.shields.io/badge/Alembic-1.11+-yellow)](https://alembic.sqlalchemy.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7.0+-red)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker-Latest-blue)](https://www.docker.com/)

![Project Screenshot Placeholder](https://i.imgur.com/sFaMPUG.png)

This is a Telegram bot designed to help students and staff of UkrDUZT access their university schedule easily. The bot provides quick and intuitive access to schedules directly within Telegram.

## Features

- 📅 **View the university schedule for different groups and faculties.**
- 📱 **Intuitive and user-friendly interface.**
- 🐍 **Built with modern Python features and tools.**

## Installation and Setup

Follow these steps to set up and run the project:

### Prerequisites

Ensure you have the following installed on your system:

- **Python 3.12**
- **Docker**
- **PostgreSQL**
- **Redis**
- **Git**

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/bubblecrabs/ukrduzt-schedule-bot.git
   cd ukrduzt-schedule-bot
   ```

2. **Set Up a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**

   Rename the `.env.example` file to `.env` and replace the placeholder values with your own data:
   
   ```bash
   mv .env.example .env
   ```   

   Example `.env` file:
   ```env
   BOT_TOKEN=1234567890:abcdefghijklmnopqrstuvwxyz
   ```

5. **Initialize the Database**

   ```bash
   alembic upgrade head
   ```

6. **Run the Bot Locally**

   ```bash
   cd bot
   python __main__.py
   ```

### Using Docker

1. **Clone the Repository**

   ```bash
   git clone https://github.com/bubblecrabs/ukrduzt-schedule-bot.git
   cd ukrduzt-schedule-bot
   ```

2. **Set Up Environment Variables**

   Rename the `.env.example` file to `.env` and replace the placeholder values with your own data:
   
   ```bash
   mv .env.example .env
   ```   

   Example `.env` file:
   ```env
   BOT_TOKEN=1234567890:abcdefghijklmnopqrstuvwxyz
   ```

3. **Run the Container**

   ```bash
   docker compose up -d --build
   docker ps
   ```

4. **Run Database Migrations**

   ```bash
   docker compose exec bot alembic upgrade head
   ```

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to improve the project.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
