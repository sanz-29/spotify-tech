def test_playlist_song_relationship_can_be_added_and_removed(
    client,
    user_factory,
    auth_headers,
):
    user_factory("artist", "artist@example.com", role="artist")
    user_factory("admin", "admin@example.com", role="admin")
    artist_headers = auth_headers(client, "artist", "password123")
    admin_headers = auth_headers(client, "admin", "password123")

    artist = client.post(
        "/artists/",
        headers=artist_headers,
        json={"name": "Relationship Artist"},
    ).json()
    genre = client.post(
        "/genres/",
        headers=admin_headers,
        json={"name": "Relationship Genre"},
    ).json()
    album = client.post(
        "/albums/",
        headers=artist_headers,
        json={"title": "Relationship Album", "artist_id": artist["artist_id"]},
    ).json()
    song = client.post(
        "/songs/",
        headers=artist_headers,
        json={
            "title": "Relationship Song",
            "artist_id": artist["artist_id"],
            "album_id": album["album_id"],
            "genre_id": genre["genre_id"],
            "audio_url": "/music/test.mp3",
            "duration": 180,
        },
    ).json()
    playlist = client.post(
        "/playlists/",
        headers=artist_headers,
        json={"name": "Relationship Playlist"},
    ).json()

    added = client.post(
        f"/playlists/{playlist['playlist_id']}/songs",
        headers=artist_headers,
        json={"song_id": song["song_id"]},
    )
    assert added.status_code == 201
    listed = client.get(
        f"/playlists/{playlist['playlist_id']}/songs",
        headers=artist_headers,
    )
    assert listed.status_code == 200
    assert listed.json()[0]["song_id"] == song["song_id"]

    removed = client.delete(
        f"/playlists/{playlist['playlist_id']}/songs/{song['song_id']}",
        headers=artist_headers,
    )
    assert removed.status_code == 200
    assert client.get(
        f"/playlists/{playlist['playlist_id']}/songs",
        headers=artist_headers,
    ).json() == []
