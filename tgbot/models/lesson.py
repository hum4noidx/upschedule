from dataclasses import dataclass


@dataclass
class Lesson:
    day_of_week: int
    lesson_number: int
    subject: str
    room: str
