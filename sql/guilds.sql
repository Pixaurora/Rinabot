CREATE TABLE guilds(
    id bigint PRIMARY KEY,
    name text,
    icon_hash text
);

CREATE TABLE guild_prefixes(
    guild_id bigint PRIMARY KEY references guilds(id),
    prefixes text[] DEFAULT '{}'
);
