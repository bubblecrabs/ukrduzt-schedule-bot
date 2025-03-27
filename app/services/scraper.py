from time import time
from aiohttp import ClientSession

from bs4 import BeautifulSoup


base_url = "http://rasp.kart.edu.ua/schedule"
headers = {
    "Accept": "*/*",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}


async def get_faculties() -> dict:
    async with ClientSession() as session:
        async with session.get(url=base_url, headers=headers) as response:
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            result = soup.select("#schedule-search-faculty option")
            faculties = {faculty["value"]: faculty.text for faculty in result if faculty.get("value")}
            return faculties


async def get_groups(year_id: int, faculty: int, course: int) -> dict:
    url = f"{base_url}/jdata"
    data = f"year_id={year_id}&faculty_id={faculty}&course_id={course}"

    async with ClientSession() as session:
        async with session.post(url=url, headers=headers, data=data) as response:
            json = await response.json()
            groups = {team["id"]: team["title"] for team in json.get("teams", [])}
            return groups


async def get_schedule(year: int, semester: int, faculty: int, course: int, group: int, day: int) -> tuple[dict, dict]:
    url = f"{base_url}/jsearch?year_id={year}&semester_id={semester}&faculty_id={faculty}&course_id={course}&team_id={group}"
    data = f"_search=false&nd={round(time())}&rows=20&page=1&sidx=&sord=asc"
    subjects_paired = {}
    subjects_unpaired = {}
    previous_pair_number = None

    async with ClientSession() as session:
        async with session.post(url=url, headers=headers, data=data) as response:
            json = await response.json()
            for subject in json.get("rows", []):
                row = subject["cell"]
                pair_number = row[0] if row[0] else previous_pair_number
                week = row[1]
                subject_name = row[day]

                if subject_name and subject_name.strip():
                    if week == "парн.":
                        subjects_paired[pair_number] = subject_name
                    elif week == "непарн.":
                        subjects_unpaired[pair_number] = subject_name
                if row[0]:
                    previous_pair_number = row[0]

    return subjects_paired, subjects_unpaired
