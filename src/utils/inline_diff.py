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
import re

_differ = difflib.Differ()

_MARKDOWN_ESCAPE_COMMON = r"^>(?:>>)?\s|\[.+\]\(.+\)"

_MARKDOWN_ESCAPE_SUBREGEX = "|".join(
    r"\{0}(?=([\s\S]*(\{0}?\{0}?)))".format(c) for c in ("*", "`", "_", "~", "|")
)

_URL_REGEX = (
    r"""(<)?(?P<url>(?:https?|steam):\/\/[^\s<]+[^<.,:;"'\]\s])(?(1)(?=(>))|)"""
)

_MENTION_REGEX = (
    r"""(<#[0-9]+>|<@!?[0-9]+>|<a?:[\w\d]+:[0-9]+>|<@&[0-9]+>|%s)""" % _URL_REGEX
)

_DIFF_STRING = """
**b:** {before}
**a:** {after}
"""

_MARKDOWN_ESCAPE_REGEX = re.compile(
    r"(?P<markdown>%s|%s)" % (_MARKDOWN_ESCAPE_SUBREGEX, _MARKDOWN_ESCAPE_COMMON),
    re.MULTILINE,
)


def prepare_text(text):
    text = re.sub(r"\\", r"\\\\", text)
    text = _MARKDOWN_ESCAPE_REGEX.sub(r"\\\1", text)

    return "\\".join(
        re.sub(_URL_REGEX, r"<\g<url>>", section) for section in text.split("\\")
    )


def inline_diff(before, after):
    before, after = (list(prepare_text(text)) for text in (before, after))

    diff = list(_differ.compare(before, after))

    before_deltas, after_deltas = (
        [i[0] for i in diff if i[0] != delta] for delta in ["+", "-"]
    )

    for match in re.finditer(_MENTION_REGEX, "".join(before)):
        span = match.span(0)
        if "-" in before_deltas[span[0] : span[1]]:
            before_deltas[span[0] : span[1]] = ["-"] * (span[1] - span[0])

    for match in re.finditer(_MENTION_REGEX, "".join(after)):
        span = match.span(0)
        if "+" in after_deltas[span[0] : span[1]]:
            after_deltas[span[0] : span[1]] = ["+"] * (span[1] - span[0])

    for match in re.finditer(r"([-]+)", "".join(before_deltas)):
        before[match.start() : match.end()] = (
            ["~~"] + before[match.start() : match.end()] + ["~~"]
        )

    for match in re.finditer(r"([+]+)", "".join(after_deltas)):
        after[match.start() : match.end()] = (
            ["**"] + after[match.start() : match.end()] + ["**"]
        )

    return _DIFF_STRING.format(before="".join(before), after="".join(after))
