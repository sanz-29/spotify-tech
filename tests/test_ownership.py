def test_artist_cannot_modify_another_artists_profile(
    client,
    user_factory,
    auth_headers,
):
    user_factory("artist_a", "artist_a@example.com", role="artist")
    user_factory("artist_b", "artist_b@example.com", role="artist")
    headers_a = auth_headers(client, "artist_a", "password123")
    headers_b = auth_headers(client, "artist_b", "password123")

    created = client.post(
        "/artists/",
        headers=headers_a,
        json={"name": "Artist A", "bio": "A"},
    )
    assert created.status_code == 201
    artist_id = created.json()["artist_id"]

    update = client.put(
        f"/artists/{artist_id}",
        headers=headers_b,
        json={"name": "Hijacked", "bio": "B"},
    )
    delete = client.delete(f"/artists/{artist_id}", headers=headers_b)

    assert update.status_code == 403
    assert delete.status_code == 403


def test_user_cannot_access_another_users_playlist(
    client,
    user_factory,
    auth_headers,
):
    user_factory("owner", "owner@example.com")
    user_factory("visitor", "visitor@example.com")
    owner_headers = auth_headers(client, "owner", "password123")
    visitor_headers = auth_headers(client, "visitor", "password123")

    created = client.post(
        "/playlists/",
        headers=owner_headers,
        json={"name": "Private playlist"},
    )
    playlist_id = created.json()["playlist_id"]

    assert client.get(
        f"/playlists/{playlist_id}",
        headers=visitor_headers,
    ).status_code == 403
    assert client.put(
        f"/playlists/{playlist_id}",
        headers=visitor_headers,
        json={"name": "Changed"},
    ).status_code == 403
    assert client.delete(
        f"/playlists/{playlist_id}",
        headers=visitor_headers,
    ).status_code == 403
