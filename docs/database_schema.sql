CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user'
);

CREATE TABLE artists (
    artist_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL UNIQUE,
    name VARCHAR(100) NOT NULL UNIQUE,
    bio TEXT NULL,
    image_url VARCHAR(255) NULL,
    CONSTRAINT fk_artists_user
        FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE genres (
    genre_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE albums (
    album_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    artist_id INT NULL,
    release_date DATE NULL,
    cover_image_url VARCHAR(255) NULL,
    CONSTRAINT fk_albums_artist
        FOREIGN KEY (artist_id) REFERENCES artists(artist_id)
);

CREATE TABLE songs (
    song_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    artist_id INT NOT NULL,
    album_id INT NULL,
    genre_id INT NULL,
    audio_url VARCHAR(255) NOT NULL,
    cover_image_url VARCHAR(255) NULL,
    duration INT NOT NULL,
    CONSTRAINT fk_songs_artist
        FOREIGN KEY (artist_id) REFERENCES artists(artist_id),
    CONSTRAINT fk_songs_album
        FOREIGN KEY (album_id) REFERENCES albums(album_id),
    CONSTRAINT fk_songs_genre
        FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
);

CREATE TABLE playlists (
    playlist_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(255) NULL,
    user_id INT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_playlists_user
        FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE playlist_songs (
    playlist_id INT NOT NULL,
    song_id INT NOT NULL,
    added_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (playlist_id, song_id),
    CONSTRAINT fk_playlist_songs_playlist
        FOREIGN KEY (playlist_id) REFERENCES playlists(playlist_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_playlist_songs_song
        FOREIGN KEY (song_id) REFERENCES songs(song_id)
        ON DELETE CASCADE
);
