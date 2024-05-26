#!/usr/bin/env python3

import requests

token = "Bearer "


def test():
    response = requests.get(
        "https://api.clashofclans.com/v1/clans/%232GV9CYLQ8",
        headers={"Authorization": token}
    )
    obj = response.json()
    for member in obj["memberList"]:
        print(member["name"])

    # for k, v in obj.items():
    #     print(k + " " + str(v))


if __name__ == "__main__":
    test()
