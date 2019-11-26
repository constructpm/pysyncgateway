def test_existing_user(existing_user, database):
    result = existing_user

    assert database.all_users() == [result]
    assert result.retrieved is False
