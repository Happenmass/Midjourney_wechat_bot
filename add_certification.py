import json

num = 10
f = json.load(open("certification.json", "r"))
with open("certification.json", "w") as file:
    for i in range(num):
        f[str(i)+"xeo"] = {"limits":f[str(i)+"xeo"]["limits"]+10, "last_message_id":"", "last_meassage_hash":""}
    json.dump(f, file)