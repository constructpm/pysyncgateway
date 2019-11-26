def test(admin_client, syncgateway_version_str):
    result = admin_client.get_server()

    assert isinstance(result, dict)
    assert sorted(list(result)) == [
        "ADMIN",
        "couchdb",
        "vendor",
        "version",
    ]
    assert result["ADMIN"] is True
    assert result["version"].startswith("Couchbase Sync Gateway/{}(".format(syncgateway_version_str))
