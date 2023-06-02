
walker get_webhook_url {
    has token;
    has url;
    has proxy_url;
    has name;
    can webhook.webhook_url;

    grph = jaseci.graph_active_get();
    if(!grph): report "Graph not found!";
    _url = webhook.webhook_url(grph['jid'], token, url, proxy_url, name);
    report _url;
}

// walker run get_webhook_url -ctx  "{\"token\" : \"95613b486641cf02ca1fd4aa94c8d5955f4d1a51afa9ff30ed7372ed740c8ade\", \"url\" : \"http://0.0.0.0:8002\", \"proxy_url\" : \"https://aef2-190-93-37-86.ngrok-free.app\", \"name\": \"interact\"}"
