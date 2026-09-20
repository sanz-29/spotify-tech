def test_artist_album_song_and_genre_crud(
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
        json={"name": "CRUD Artist"},
    ).json()
    assert client.get(f"/artists/{artist['artist_id']}").status_code == 200
    updated_artist = client.put(
        f"/artists/{artist['artist_id']}",
        headers=artist_headers,
        json={"name": "Updated CRUD Artist"},
    )
    assert updated_artist.status_code == 200

    album = client.post(
        "/albums/",
        headers=artist_headers,
        json={"title": "CRUD Album", "artist_id": artist["artist_id"]},
    ).json()
    assert client.get(f"/albums/{album['album_id']}").status_code == 200
    assert client.put(
        f"/albums/{album['album_id']}",
        headers=artist_headers,
        json={
            "title": "Updated CRUD Album",
            "artist_id": artist["artist_id"],
        },
    ).status_code == 200

    genre = client.post(
        "/genres/",
        headers=admin_headers,
        json={"name": "CRUD Genre"},
    ).json()
    assert client.get(f"/genres/{genre['genre_id']}").status_code == 200
    assert client.put(
        f"/genres/{genre['genre_id']}",
        headers=admin_headers,
        json={"name": "Updated CRUD Genre"},
    ).status_code == 200

    song = client.post(
        "/songs/",
        headers=artist_headers,
        json={
            "title": "CRUD Song",
            "artist_id": artist["artist_id"],
            "album_id": album["album_id"],
            "genre_id": genre["genre_id"],
            "audio_url": "/music/test.mp3",
            "duration": 200,
        },
    ).json()
    assert client.get(f"/songs/{song['song_id']}").status_code == 200
    assert client.put(
        f"/songs/{song['song_id']}",
        headers=artist_headers,
        json={
            "title": "Updated CRUD Song",
            "artist_id": artist["artist_id"],
            "album_id": album["album_id"],
            "genre_id": genre["genre_id"],
            "audio_url": "/music/test.mp3",
            "duration": 201,
        },
    ).status_code == 200

    assert client.delete(
        f"/songs/{song['song_id']}",
        headers=artist_headers,
    ).status_code == 200
    assert client.delete(
        f"/albums/{album['album_id']}",
        headers=artist_headers,
    ).status_code == 200
    assert client.delete(
        f"/genres/{genre['genre_id']}",
        headers=admin_headers,
    ).status_code == 200
    assert client.delete(
        f"/artists/{artist['artist_id']}",
        headers=artist_headers,
    ).status_code == 200


def test_playlist_owner_can_complete_crud_flow(
    client,
    user_factory,
    auth_headers,
):
    user_factory("listener", "listener@example.com")
    headers = auth_headers(client, "listener", "password123")

    created = client.post(
        "/playlists/",
        headers=headers,
        json={"name": "CRUD Playlist"},
    )
    assert created.status_code == 201
    playlist_id = created.json()["playlist_id"]

    assert client.get("/playlists/", headers=headers).status_code == 200
    assert client.get(
        f"/playlists/{playlist_id}",
        headers=headers,
    ).status_code == 200
    assert client.put(
        f"/playlists/{playlist_id}",
        headers=headers,
        json={"name": "Updated CRUD Playlist"},
    ).status_code == 200
    assert client.delete(
        f"/playlists/{playlist_id}",
        headers=headers,
    ).status_code == 200


def test_invalid_input_returns_validation_error(client):
    response = client.post(
        "/users/",
        json={
            "username": "listener",
            "email": "not-an-email",
            "password": "password123",
        },
    )

    assert response.status_code == 422
