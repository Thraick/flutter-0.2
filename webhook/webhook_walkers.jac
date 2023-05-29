
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

// walker run get_webhook_url -ctx  "{\"token\" : \"b303f4f3a15e652ba6167161b071b8cb5cb2289c352992cd8f17708abadae59b\", \"url\" : \"http://0.0.0.0:8002\", \"proxy_url\" : \"https://f1d5-190-93-37-91.ngrok-free.app\", \"name\": \"interact\"}"
