"""
Rina Bot: Discord Bot for Something Probably
Copyright (C) 2020 Rina

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import random
import re

from ..errors import BadDieAmount, BadDieName, BadDieSides


class Die:
    __slots__ = ("amount", "faces", "name")

    def __init__(self, name: str):
        result = re.compile(r"^(\d+)d(\d+)$").findall(name)

        if not result:
            raise BadDieName

        amount, faces = (int(i) for i in result[0])

        if amount <= 0:
            raise BadDieAmount

        if faces <= 0:
            raise BadDieSides

        self.amount = amount
        self.faces = faces

    def roll(self):
        return [random.randint(1, self.faces) for i in range(self.amount)]

    def __str__(self):
        return f"{self.amount}d{self.faces}"
