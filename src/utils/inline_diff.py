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

import difflib
import inspect
import re

from discord import utils

_differ = difflib.Differ()

_LINK_REGEX = r"""((?:https?|steam):\/\/[^\s<]+[^<.,:;"'\]\s])"""

_MENTION_REGEX = r"""^(<#[0-9]+>|<@!?[0-9]+>|<a?:[\w\d]+:[0-9]+>|<@&[0-9]+>|<(?:(?:https?|steam):\/\/[^\s<]+[^<.,:;"'\]\s])>)"""


def check_for_mentions(text):
    return re.findall(_MENTION_REGEX, text)


def inline_diff(before, after):
    before, after = (
        re.sub(_LINK_REGEX, r"<\1>", utils.escape_markdown(text))
        for text in (before, after)
    )

    diff = list(_differ.compare(before, after))

    deltas = [i[0] for i in diff]
    last_deltas = [""] + deltas[:-1]
    next_deltas = deltas[1:] + [""]
    characters = [i[2] for i in diff]

    allow_format_change = True
    override_before_delta = False
    override_after_delta = False
    end_of_mention = 0

    before_output = ""
    after_output = ""

    for i, last_delta, delta, next_delta, character in zip(
        range(len(diff)), last_deltas, deltas, next_deltas, characters
    ):
        if character == "<":
            possible_mention = re.findall(_MENTION_REGEX, "".join(characters[i:]))

            print(possible_mention)

            if possible_mention:
                end_of_mention = i + len(possible_mention[0]) - 1
                allow_format_change = False

                override_before_delta = "-" in deltas[i:end_of_mention]
                override_after_delta = "+" in deltas[i:end_of_mention]

                if override_before_delta:
                    before_output += "~~"
                if override_after_delta:
                    after_output += "**"

        if delta != "+":
            if delta == "-" and delta != last_delta and allow_format_change:
                before_output += "~~"
            before_output += character
            if i == end_of_mention:
                allow_format_change = True
            if (
                delta == "-"
                and delta != next_delta
                and allow_format_change
                or allow_format_change
                and override_before_delta
            ):
                before_output += "~~"
                override_before_delta = False
        if delta != "-":
            if delta == "+" and delta != last_delta and allow_format_change:
                after_output += "**"
            after_output += character
            if (
                delta == "+"
                and delta != next_delta
                and allow_format_change
                or allow_format_change
                and override_after_delta
            ):
                after_output += "**"
                override_after_delta = False

    return inspect.cleandoc(
        """
        **b:** {before}
        **a:** {after}
        """
    ).format(before=before_output, after=after_output)
