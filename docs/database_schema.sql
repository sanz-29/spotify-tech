CREATE TABLE IF NOT EXISTS albums (
    album_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    artist_id INT,
    release_date DATE,
    cover_image_url VARCHAR(255),
    FOREIGN KEY (artist_id) REFERENCES artists(artist_id)
);

CREATE TABLE IF NOT EXISTS genres (
    genre_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);