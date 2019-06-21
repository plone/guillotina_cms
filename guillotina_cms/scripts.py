import requests


def initdb():
    groot = "http://localhost:8081/db"

    # Create container
    resp = requests.post(
        groot,
        auth=("root", "root"),
        json={"@type": "Container", "id": "web", "title": "Guillotina CMS Site"},
    )
    assert resp.status_code in (200, 409)

    # Install CMS package
    resp = requests.post(
        "{}/web/@addons".format(groot), auth=("root", "root"), json={"id": "cms"}
    )
    assert resp.status_code in (200, 412)

    # Install DB users package
    resp = requests.post(
        "{}/web/@addons".format(groot), auth=("root", "root"), json={"id": "dbusers"}
    )

    assert resp.status_code in (200, 412)

    # Create initial user
    payload = {
        "@type": "User",
        "username": "admin",
        "email": "foo@bar.com",
        "password": "admin",
    }
    resp = requests.post("{}/web/users".format(groot), auth=("root", "root"), json=payload)

    assert resp.status_code == 201

    # Grant initial permissions to admin user
    resp = payload = {
        "roleperm": [
            {
                "setting": "AllowSingle",
                "role": "guillotina.Anonymous",
                "permission": "guillotina.ViewContent",
            },
            {
                "setting": "AllowSingle",
                "role": "guillotina.Anonymous",
                "permission": "guillotina.AccessContent",
            },
        ],
        "prinrole": [
            {"setting": "Allow", "role": "guillotina.Manager", "principal": "admin"},
            {"setting": "Allow", "role": "guillotina.Owner", "principal": "admin"},
        ],
    }
    resp = requests.post("{}/web/@sharing".format(groot), auth=("root", "root"), json=payload)

    assert(resp.status_code == 200)


def deletedb():
    groot = "http://localhost:8081/db"

    resp = requests.delete("{}/web".format(groot), auth=("root", "root"))

    assert(resp.status_code == 200)
