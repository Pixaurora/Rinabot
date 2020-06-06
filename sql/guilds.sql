CREATE TABLE guilds(
    guild_id bigint PRIMARY KEY,
    logging_enabled bool DEFAULT false,
    logging_channel bigint
)