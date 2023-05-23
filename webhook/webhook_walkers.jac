
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

// walker run get_webhook_url -ctx  "{\"token\" : \"b55493d9b071041071c9b030ca49e425d7211bf0896ab0168b9970488acbd03f\", \"url\" : \"http://0.0.0.0:8003\", \"proxy_url\" : \"https://d384-190-93-37-93.sa.ngrok.io\", \"name\": \"vs_recognizer\"}"
