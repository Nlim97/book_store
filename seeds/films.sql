CREATE TABLE IF NOT EXISTS films (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title TEXT NOT NULL,
    year INTEGER NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS films_title_year_unique_idx
    ON films (title, year);

TRUNCATE table films;

INSERT INTO films (title, year) VALUES
    ('The Gruffalo', 2009),
    ('Ada Twist, Scientist', 2021),
    ('The Girl Who Drank the Moon', 2020),
    ('Dragons in a Bag', 2019)
ON CONFLICT (title, year) DO NOTHING;