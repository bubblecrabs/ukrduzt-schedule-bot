import time
from datetime import datetime, date

import httpx
from bs4 import BeautifulSoup


class ScheduleScraper:
    BASE_URL = "http://rasp.kart.edu.ua/schedule"
    TIMEOUT = 30

    HEADERS = {
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }

    EMOJI_MAP = {
        1: "1️⃣",
        2: "2️⃣",
        3: "3️⃣",
        4: "4️⃣",
        5: "5️⃣",
        6: "6️⃣",
        7: "7️⃣",
        8: "8️⃣",
        9: "9️⃣",
        10: "🔟",
    }

    def __init__(self, timeout: int = TIMEOUT):
        self.timeout = httpx.Timeout(timeout)

    async def get_faculties(self) -> dict[str, str]:
        """Get the faculties from the website."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(self.BASE_URL, headers=self.HEADERS)
                response.raise_for_status()
                html = response.text
                return self._parse_faculties(html)

        except Exception as e:
            raise Exception(f"Failed to get faculties: {e}")

    def _parse_faculties(self, response: str) -> dict[str, str]:
        """Parse the faculties from the website."""
        try:
            soup = BeautifulSoup(response, "html.parser")
            faculty_options = soup.select("#schedule-search-faculty option")

            faculties = {}
            for option in faculty_options:
                faculty_id = option.get("value")
                if faculty_id:
                    faculties[faculty_id] = option.text.strip()

            return faculties

        except Exception as e:
            raise Exception(f"Failed to parse faculties: {e}")

    async def get_groups(self, year_id: int, faculty: int, course: int) -> dict[int, str]:
        """Get the groups from the website."""
        url = f"{self.BASE_URL}/jdata"
        data = f"year_id={year_id}&faculty_id={faculty}&course_id={course}"

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, headers=self.HEADERS, data=data)
                response.raise_for_status()
                json_data = response.json()

            return self._parse_groups(json_data)

        except Exception as e:
            raise Exception(f"Failed to get groups: {e}")

    def _parse_groups(self, response: dict) -> dict[int, str]:
        """Parse the groups from the website."""
        try:
            teams = response.get("teams", [])
            return {team["id"]: team["title"] for team in teams if "id" in team and "title" in team}

        except Exception as e:
            raise Exception(f"Failed to parse groups: {e}")

    async def get_schedule(
        self, year: int, semester: int, faculty: int, course: int, group: int, day: int
    ) -> tuple[dict[int, str], dict[int, str]]:
        """Get the schedule from the website."""
        url = f"{self.BASE_URL}/jsearch?year_id={year}&semester_id={semester}&faculty_id={faculty}&course_id={course}&team_id={group}"
        data = f"_search=false&nd={round(time.time())}&rows=20&page=1&sidx=&sord=asc"

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, headers=self.HEADERS, data=data)
                response.raise_for_status()
                json_data = response.json()

            return self._parse_schedule(json_data, day)

        except Exception as e:
            raise Exception(f"Failed to get schedule: {e}")

    def _parse_schedule(self, response: dict, day: int) -> tuple[dict[int, str], dict[int, str]]:
        """Parse the schedule from the website."""
        try:
            paired_subjects = {}
            unpaired_subjects = {}
            previous_pair_number = None

            rows = response.get("rows", [])

            for subject in rows:
                cell = subject.get("cell", [])
                if len(cell) <= day:
                    continue

                pair_number = cell[0] if cell[0] else previous_pair_number
                week_type = cell[1] if len(cell) > 1 else ""
                subject_name = cell[day] if len(cell) > day else ""

                if subject_name and subject_name.strip():
                    if week_type == "парн.":
                        paired_subjects[pair_number] = subject_name.strip()
                    elif week_type == "непарн.":
                        unpaired_subjects[pair_number] = subject_name.strip()

                if cell[0]:
                    previous_pair_number = cell[0]

            return paired_subjects, unpaired_subjects

        except Exception as e:
            raise Exception(f"Failed to parse schedule: {e}")

    @staticmethod
    def is_weekend() -> bool:
        """Check if today is a weekend."""
        return datetime.today().weekday() >= 5

    @staticmethod
    def get_current_week_parity() -> str:
        """Get current week parity."""
        today = date.today()
        week_number = today.isocalendar()[1]
        return "Непарна" if week_number % 2 != 0 else "Парна"

    def _replace_numbers_with_emojis(self, schedule: dict[int, str]) -> dict[str, str]:
        """Replace numeric keys with emoji equivalents."""
        return {self.EMOJI_MAP.get(key, str(key)): value for key, value in schedule.items()}

    def format_schedule_message(
        self,
        paired_subjects: dict[int, str],
        unpaired_subjects: dict[int, str],
        selected_day: str,
        user_group_name: str,
    ) -> str:
        """Format schedule message."""
        is_weekend = self.is_weekend()
        selected_week = "наступний" if is_weekend else "цей"
        current_week = self.get_current_week_parity()

        if is_weekend:
            next_week_is_even = current_week == "Непарна"
            selected_subjects = paired_subjects if next_week_is_even else unpaired_subjects
        else:
            selected_subjects = paired_subjects if current_week == "Парна" else unpaired_subjects

        formatted_subjects = self._replace_numbers_with_emojis(selected_subjects)
        subjects_text = "\n".join(f"{pair}: <b>{subject}</b>" for pair, subject in formatted_subjects.items())

        message_text = f"🔔 Показано розклад на <b>{selected_week}</b> тиждень!\n\n"

        if subjects_text:
            message_text += f"{subjects_text}\n\n"
        else:
            message_text += "🔍 На <b>цей</b> день ваш розклад вільний.\n\n"

        message_text += (
            f"⏰ Вибраний день — <b>{selected_day}</b>\n"
            f"📆 Поточна неділя — <b>{current_week}</b>\n"
            f"💼 Вибрана група — <b>{user_group_name}</b>"
        )

        return message_text


scraper = ScheduleScraper()
