"""
Rina Bot: Discord Bot for Something Probably
Copyright (c) 2016 - 2020 Lilly Rose Berner

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

import re

from ..cogs.errors.formatting import remove_accents


def clean_prefix(bot, prefix):
    # Replace emoji and mentions with their rendered counterparts
    # Otherwise users are shown the raw form due to the code block

    prefix = re.sub(r"<a?:(\w{2,32}):\d{15,21}>", ":\\1:", prefix)  # Emoji
    prefix = re.sub(fr"<@!?{bot.user.id}>", f"@{bot.user}", prefix)  # Mentions

    return remove_accents(prefix)
