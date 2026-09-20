def test_normal_user_cannot_access_admin_endpoints(
    client,
    user_factory,
    auth_headers,
):
    user_factory("listener", "listener@example.com")
    headers = auth_headers(client, "listener", "password123")

    response = client.get("/admin/users", headers=headers)

    assert response.status_code == 403


def test_admin_can_access_admin_endpoints(client, user_factory, auth_headers):
    admin = user_factory("admin", "admin@example.com", role="admin")
    headers = auth_headers(client, admin.username, "password123")

    response = client.get("/admin/users", headers=headers)

    assert response.status_code == 200
    assert any(item["username"] == "admin" for item in response.json())
