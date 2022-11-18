from bs4 import BeautifulSoup
import requests


class ProgrammYar:
    name: str = None
    time_data: str = None
    description: str = None
    link: str = None
    period: str = None


class ParserProgram:
    def __init__(self) -> None:

        self.list_data: list = []
        self.flag: bool = True
        self.i = 0

        url = "https://smartyar.timepad.ru/events/"
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        self.list_event = soup.find_all("div", {"class": "__c"})
        self.parser_data()

    def parser_data(self):
        for i in range(0, len(self.list_event), 2):
            self.i = i
            try:
                time_data = self.list_event[self.i + 1].find_all(
                    "span",
                    {"class": "t-card_event__glance"}
                )[0].text.strip().split(", ")[-1]
            except Exception as e:
                e
                time_data = self.list_event[self.i + 1].find_all(
                    "span",
                    {"class": "t-card_event__now"}
                )[0].text.strip().split(", ")[-1]

            if "назад" in time_data:
                break
            else:
                prog: ProgrammYar = ProgrammYar()
                prog.time_data = time_data
                prog.name = self.parser_name()
                prog.description = self.parser_description()
                prog.period = self.parser_period()
                prog.link = self.parser_link()

            self.list_data.append(prog)

    def parser_name(self):
        return self.list_event[self.i].find_all("a")[0].text.strip()

    def parser_description(self):
        return self.list_event[self.i + 1].find_all(
            "p",
            {"class": "t-description"}
        )[0].text.strip()

    def parser_link(self):
        return self.list_event[self.i + 1].find_all(
            "a",
            href=True
        )[0]["href"]

    def parser_period(self):
        period = self.list_event[self.i + 1].find_all(
            "p",
            {"class": "t-card_event__info"}
        )[0].text.strip()
        period = period.split(", ")[0].split("Ярославль  ")[-1]
        return period

    def get_data(self) -> list:
        return self.list_data
