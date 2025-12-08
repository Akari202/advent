import json
import logging
import os
import re
import sys
from datetime import datetime, timedelta
from enum import Enum
from logging import debug, error, info, warning
from pathlib import Path
from typing import Any, Callable, cast, Optional

import colorlog
import requests
from colorlog import ColoredFormatter
from dotenv import load_dotenv
from requests.models import Response

from .errors import (
    ErrorFetchingAnswers,
    ErrorFetchingInput,
    ErrorSubmitting,
    SessionError,
    UnknownResponse,
    UnreachableError,
)

try_load_env = load_dotenv()
if not try_load_env:
    _ = load_dotenv(Path(sys.argv[0]).resolve().parent.parent / ".env")

DEV_MODE = os.getenv("DEV_MODE") == "True"
# DEV_MODE = True
SESSION = os.getenv("SESSION")
if SESSION is None:
    raise SessionError
if DEV_MODE:
    info("Running in development mode")
handler = colorlog.StreamHandler()
formatter = ColoredFormatter(
    "%(log_color)s[%(levelname)s]%(reset)s %(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red,bg_white",
    },
    secondary_log_colors={},
    style="%",
)
logger = logging.getLogger()
# if DEV_MODE:
#     logger.setLevel(logging.DEBUG)
# else:
#     logger.setLevel(logging.INFO)
#     sys.tracebacklimit = 0
logger.setLevel(logging.DEBUG)
if not DEV_MODE:
    sys.tracebacklimit = 0
handler.setFormatter(formatter)
logger.handlers = []
logger.addHandler(handler)
__puzzle_attr = None
headers = {
    "User-Agent": "python-requests, Akari202 aoc library <akaritwo0two@gmail.com>"
}


class Part(Enum):
    ONE = 1
    TWO = 2


class Result(Enum):
    CORRECT = 0
    HIGH = 1
    LOW = 2
    COMPLETED = 3

    def to_function(self) -> Callable[[int, int], int]:
        if self == Result.HIGH:
            return min
        if self == Result.LOW:
            return max
        if self == Result.COMPLETED:
            raise UnreachableError

        def dummy(arg1: int, _arg2: int) -> int:
            error("Something really goofy happened. Continuing")
            return arg1

        return dummy


def cmp_correct(correct: int, guess: int) -> Result:
    if correct == guess:
        return Result.CORRECT
    elif correct > guess:
        return Result.LOW
    else:
        return Result.HIGH


class Aoc:
    def __init__(self):
        self.path: Path = Path(sys.argv[0]).resolve()
        self.year: int = int(self.path.parent.name)
        self.day: int = int(self.path.stem)
        self.input_file: Path = self.path.parent / "data" / f"{self.day} input"
        self.cache_file: Path = self.path.parent / "data" / f"{self.day} cache"
        self.test_file: Path = self.path.parent / "data" / f"{self.day} test"
        self.__input_data = ""
        self.__is_test = False
        self.__test_answers: list[int] = [0, 0]
        info(f"Using {self.year} day {self.day}")
        debug(f"Using session id: {SESSION}")
        data_dir = self.path.parent / "data"
        data_dir.mkdir(exist_ok=True)

    def __str__(self) -> str:
        return f"{self.year} day {self.day}"

    @property
    def input(self) -> str:
        if self.__input_data == "":
            if self.is_input_cached():
                self.__input_data = self.__read_input()
            else:
                self.__input_data = self.__get_input()
                self.__cache_input()
        return self.__input_data

    @property
    def test_answer_one(self) -> int:
        return self.__test_answers[0]

    @test_answer_one.setter
    def test_answer_one(self, value: int):
        self.__input_data = ""
        self.__is_test = True
        self.__test_answers[0] = value

    @property
    def test_answer_two(self) -> int:
        return self.__test_answers[1]

    @test_answer_two.setter
    def test_answer_two(self, value: int):
        self.__input_data = ""
        self.__is_test = True
        self.__test_answers[1] = value

    def is_test(self) -> bool:
        return self.__is_test

    def test_answer(self, part: Part) -> int:
        match part:
            case Part.ONE:
                return self.__test_answers[0]
            case Part.TWO:
                return self.__test_answers[1]

    def is_input_cached(self) -> bool:
        if self.is_test():
            return self.test_file.is_file()
        else:
            return self.input_file.is_file()

    def lines(self) -> list[str]:
        return [i.strip() for i in self.input.splitlines()]

    def csv_lines(self) -> list[list[str]]:
        return [[j.strip() for j in i.split(",")] for i in self.input.splitlines()]

    def csv_values(self) -> list[list[int]]:
        return [[int(j.strip()) for j in i.split(",")] for i in self.input.splitlines()]

    def char_grid(self) -> list[list[str]]:
        return [list(i.strip()) for i in self.input.splitlines()]

    def submit_one(self, answer: int):
        self.__submit(Part.ONE, answer)

    def submit_two(self, answer: int):
        self.__submit(Part.TWO, answer)

    def __dev_server_check(self) -> bool:
        if DEV_MODE:
            response = input(
                "Dev: Do you really want to request from the server? [Y/n]: "
            )
            if response == "" or response.lower() != "Y":
                return True
            else:
                return False
        return True

    def __submit(self, part: Part, answer: int):
        if self.__check_submission(part, answer):
            if not self.__dev_server_check():
                return
            info(f"Submitting {answer} to server for part {part}")
            response = requests.post(
                self.__submit_url(),
                cookies={"session": SESSION},
                headers=headers,
                data={"level": part.value, "answer": answer},
            )
            if response.status_code != 200:
                error("Unable to submit answer")
                debug(response.__dict__)
                raise ErrorSubmitting
            result = Aoc.__parse_submission_response(response)
            if result == Result.COMPLETED:
                correct_answers = self.__fetch_completed_answers()
                if correct_answers[part.value - 1] is None:
                    error(
                        "Something has gone quite wrong. "
                        + "Server seems to think this puzzle is completed but I am unable to parse the answers"
                    )
                    raise ErrorSubmitting
                result = cmp_correct(cast(int, correct_answers[part.value - 1]), answer)
                if part == Part.ONE and correct_answers[1] is not None:
                    self.__save_submission(Part.TWO, correct_answers[1], Result.CORRECT)
            if result == Result.CORRECT:
                self.__print_correct(part, answer)
            else:
                self.__print_wrong(part, answer, result)
            self.__save_submission(part, answer, result)

    @staticmethod
    def __parse_submission_response(response: Response) -> Result:
        content = str(response.content.decode("utf-8"))
        if "That's the right answer" in content:
            return Result.CORRECT
        elif "That's not the right answer; your answer is too low" in content:
            return Result.LOW
        elif "That's not the right answer; your answer is too high" in content:
            return Result.HIGH
        elif "You don't seem to be solving the right level." in content:
            error("Level already completed")
            return Result.COMPLETED
        else:
            error("Unknown response")
            debug(response.__dict__)
            raise UnknownResponse

    def __fetch_completed_answers(self) -> tuple[Optional[int], Optional[int]]:
        if not self.__check_puzzle_released():
            raise ErrorFetchingInput
        if not self.__dev_server_check():
            raise ErrorFetchingInput
        info("Fetching completed answers from server")
        response = requests.get(
            f"https://adventofcode.com/{self.year}/day/{self.day}",
            cookies={"session": SESSION},
            headers=headers,
        )
        if response.status_code != 200:
            error("Error fetching answers")
            raise ErrorFetchingAnswers
        content = response.content.decode("utf-8")
        matches = re.findall(r"Your puzzle answer was \D*(\d*)", content)
        if len(matches) == 0:
            return (None, None)
        if len(matches) == 1:
            return (int(matches[0]), None)
        if len(matches) == 2:
            return (int(matches[0]), int(matches[1]))
        error("Too many answers?????")
        error(content)
        raise UnreachableError

    def __check_puzzle_released(self) -> bool:
        now = datetime.now()
        puzzle_date = datetime(self.year, 12, self.day)
        delta = now - puzzle_date
        if delta <= timedelta(0):
            error(f"That puzzle is still in the future! Please wait {abs(delta)}")
            return False
        return True

    def __load_cache(self) -> dict[str, Any]:
        cache: dict[str, Any] = {}
        if self.cache_file.exists():
            with open(self.cache_file, "r") as file:
                cache = json.load(file)
        return cache

    def __check_submission(self, part: Part, answer: int) -> bool:
        if not self.__check_puzzle_released():
            return False

        if self.is_test():
            info("Evaluating test case")
            correct = self.test_answer(part)
            result = cmp_correct(correct, answer)
            if result == Result.CORRECT:
                info(
                    f"{answer} is the correct test answer for {self.year} day {self.day} part {part.name}"
                )
            else:
                warning(
                    f"{answer} is not the correct test answer for {self.year} day {self.day} part {part.name}. It is too {result.name}, the correct answer is {correct}"
                )
            return False

        cache = self.__load_cache()

        if part.name in cache.keys():
            if Result.CORRECT.name in cache[part.name].keys():
                correct = cache[part.name][Result.CORRECT.name]
                if answer == correct:
                    self.__print_correct(part, answer)
                else:
                    info("The correct answer, {correct}, has already been submitted")
                    self.__print_wrong(part, answer, cmp_correct(correct, answer))
                return False
            if Result.LOW.name in cache[part.name].keys():
                low = cache[part.name][Result.LOW.name]
                if answer < low:
                    info(
                        f"You have already made a higher guess, {low}, that was still too low"
                    )
                    return False
                if answer == low:
                    info(
                        f"You have already submitted that guess, {low}, and it was too low"
                    )
                    return False
            if Result.HIGH.name in cache[part.name].keys():
                high = cache[part.name][Result.HIGH.name]
                if answer > high:
                    info(
                        f"You have already made a lower guess, {high}, that was still too high"
                    )
                    return False
                if answer == high:
                    info(
                        f"You have already submitted that guess, {high}, and it was too high"
                    )
                    return False

        if "last_submit_time" in cache.keys():
            now = datetime.now()
            last_submit = datetime.fromisoformat(cache["last_submit_time"].strip())
            delta = now - last_submit
            timeout = timedelta(minutes=5)
            if delta < timeout:
                info("Too soon to submit a new answer")
                remaining = timeout - delta
                info(f"Please wait {remaining} longer")
                return False

        return True

    def __save_submission(self, part: Part, answer: int, result: Result):
        cache = self.__load_cache()
        now = datetime.now()
        cache["last_submit_time"] = now.isoformat()
        if part.name in cache.keys():
            if result.name in cache[part.name].keys():
                comp_function = result.to_function()
                cache[part.name][result.name] = comp_function(
                    answer, cache[part.name][result.name]
                )
            else:
                cache[part.name][result.name] = answer
        else:
            cache[part.name] = {result.name: answer}

        with open(self.cache_file, "w") as file:
            json.dump(cache, file)

    def __print_correct(self, part: Part, answer: int):
        info(
            f"{answer} is the correct answer for {self.year} day {self.day} part {part.name}"
        )

    def __print_wrong(self, part: Part, answer: int, result: Result):
        warning(
            f"{answer} is not the correct answer for {self.year} day {self.day} part {part.name}. It is too {result.name}"
        )

    def __cache_input(self):
        if self.is_test():
            error("Test cases were attempted to be cached. This should never happen")
            raise UnreachableError
        with open(self.input_file, "w") as file:
            file.write(self.__input_data)

    def __get_input(self) -> str:
        if not self.__check_puzzle_released():
            raise ErrorFetchingInput
        if self.is_test():
            error("Cannot automatically fetch test cases")
            raise ErrorFetchingInput
        if not self.__dev_server_check():
            raise ErrorFetchingInput
        info("Fetching input from server")
        response = requests.get(
            self.__input_url(), headers=headers, cookies={"session": SESSION}
        )
        if response.status_code != 200:
            error("Error fetching input")
            raise ErrorFetchingInput
        return response.content.decode("utf-8")

    def __read_input(self) -> str:
        info("Reading cached input")
        if self.is_test():
            with open(self.test_file, "r") as file:
                return file.read()
        else:
            with open(self.input_file, "r") as file:
                return file.read()

    def __input_url(self) -> str:
        return f"https://adventofcode.com/{self.year}/day/{self.day}/input"

    def __submit_url(self) -> str:
        return f"https://adventofcode.com/{self.year}/day/{self.day}/answer"


# __all__ = ["puzzle"]


def __getattr__(name: str) -> Aoc:
    if name == "puzzle":
        global __puzzle_attr
        if __puzzle_attr is None:
            __puzzle_attr = Aoc()
        return __puzzle_attr
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
