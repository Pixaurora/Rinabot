CREATE TABLE IF NOT EXISTS guilds(
    id bigint PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS guild_prefixes(
    guild_id bigint PRIMARY KEY references guilds(id),
    prefixes text[] DEFAULT '{}'
);
