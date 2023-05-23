from jaseci.jsorc.live_actions import jaseci_action
import requests
import json

################### update ###################

active_graph = "urn:uuid:a836fadd-729b-41b5-8de2-279acdf70035"
token_ = "b55493d9b071041071c9b030ca49e425d7211bf0896ab0168b9970488acbd03f"
url = "http://0.0.0.0:8003"
proxy_url = "https://d384-190-93-37-93.sa.ngrok.io"


################### setup ###################
# jsserv
# ngrok http 8000

# https://glitch.com/edit/#!/determined-sepia-sailboat?path=app.js%3A42%3A194
# https://developers.facebook.com/apps/985140255790427/whatsapp-business/wa-dev-console/?business_id=850390262846099


################### helper function ###################

def create_walker(url, token, name:str):
    url = url+"/js/walker_spawn_create"
    headers = {
        "Authorization": "token "+token,
        "Content-Type": "application/json"
    }
    data = {"name": name, "snt": "active:sentinel"}

    response = requests.post(url, headers=headers, data=json.dumps(data))
    print("result")
    print(response.json())
    ss = response.json()
    print(ss)
    ww = ss['jid']
    print(ww)
    result = response.json()['jid']
    print(result)
    return result


def gen_key(url: str, token: str, name:str):
    url = url+"/js/walker_get"
    headers = {
        "Authorization": "token "+token,
        "Content-Type": "application/json"
    }
    data = {"mode": "keys",
            "wlk": "spawned:walker:"+ name, "detailed": False}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    result = response.json()['anyone']
    print("result")
    print(result)
    return result


def create_url(url, node, walker: str, key: str):
    url = url+"/js_public/walker_callback/"+node+"/"+walker+"?key="+key
    print("----------url----------\n")
    print(url)
    return url


def token(token, url):
    url = url
    data = {
        "token": token
    }
    response = requests.post(url, headers=None, data=data)
    print("token")
    print(response.content)
    return response.content


def test(url: str):
    verify_token = "123"
    challenge = "111111111111111111111111111111111"
    mode = "subscribe"

    url = url
    # url = "https://dbf2-190-93-37-85.sa.ngrok.io/js_public/walker_callback/0bead0aa-2201-41c7-8ac1-c6fc284e601b/7a1a1492-015c-49e7-9974-f722d568e09c?key=79a343cc639938175b33a37f98a7a083"
    params = {
        "hub.verify_token": verify_token,
        "hub.challenge": challenge,
        "hub.mode": mode
    }

    response = requests.get(url, params=params)
    print(response.text)


################### manual #####################

# create_walker("http://localhost:8003", "ca29e26e73f69c79297b4ceada434550efeee65ca5ab8a7593fdd871b68c33f3")
# gen_key("http://localhost:8003" ,"ca29e26e73f69c79297b4ceada434550efeee65ca5ab8a7593fdd871b68c33f3")
# create_url("https://dbf2-190-93-37-85.sa.ngrok.io","c3d75e61-411e-42ff-8f51-3f95c7c29d04","c3d75e61-411e-42ff-8f51-3f95c7c29d04","883351af936ad30471ce2e29c0549051")
# token("5394a16c11455f2dadd36264ec4a3ca30c476774ee5a321af6711b662ef5915d", "https://b9e9ca262865e0c568d7f6f027173e0a.loophole.site/js_public/walker_callback/f661d2e2-dcc9-4d39-ac2d-e92667f8e819/d1e65f31-3876-45cc-a93c-3bce7bb21030?key=4f1c9b56a08c1b4cd84d9a830055d33e")
# test()
# python3 utils/model/local/webhook.py
# https://b51fcfc0bcacf8caa5f65d3011810cfe.loophole.site/js_public/walker_callback/5d7b2cb4-cdd9-459f-b124-72172d62548e/aaf9c220-9abe-4c12-af82-cef83b74f45c?key=58dd103ce288ce9137fd6bb2677a15b8


################### run #####################
@jaseci_action(act_group=["webhook"], allow_remote=True)
def webhook_url(active_graph: str, token_: str, url: str, proxy_url: str, name:str):
    if "urn:uuid:" in active_graph:
        active_graph = active_graph.replace("urn:uuid:", "")

    walker = create_walker(url, token_, name)
    if not walker:
        return "Walker not found!"
    key = gen_key(url, token_, name)
    if not walker:
        return "key not found!"
    if "urn:uuid:" in walker:
        walker = walker.replace("urn:uuid:", "")

    _url = create_url(proxy_url, active_graph, walker, key)
    if not walker:
        return "url not found!"

    return _url


# webhook_url(active_graph, token_, url, proxy_url)




