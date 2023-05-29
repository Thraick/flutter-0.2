import {*} with "graph.jac";
import {*} with "./identities/identities_walkers.jac";
import {*} with "./webhook/webhook_walkers.jac";

walker init {

    root {
        take --> node::app_root else { 
            spawn here ++> graph::app_graph; }
    }
}

walker interact: anyone {
    has image_data;
    has expression;
    
    // if (image_data){
    //     id = spawn net.root() walker::vs_recognizer(image_data=image_data);
    // }

    // expression_list = ["HAPPY","SAD","ANGRY","SUPRISE","FEAR","DISGUST"];

    // if(expression and expression not in expression_list){
    //     report:custom = {"ERROR": "Expression '"+expression+"'is not in " + expression_list.str};
    //     report:status = 404;
    // }
    // else: report expression;
    ss = spawn net.root() walker::vs_recognizer(image_data = image_data);

    std.out('ooooooooooooooooooooooooooooooooooooooooooo');
    std.out(image_data);
    std.out(expression);

    report ss;
}

walker inter {
    can file.load_json;
    has path = "";

    ww = file.load_json(path);
    // ww = file.load_json('ztest.json');
    // std.out(ww['image'][0]);

    ss = spawn net.root() walker::vs_recognizer(image_data = ww['image'][0]);
    // std.out('ooooooooooooooooooooooooooooooooooooooooooo');
    // std.out(ss);
}


/*


jac build main.jac
sentinel set -snt active:sentinel -mode ir main.jir
walker yield clear



walker yield clear
graph delete active:graph
graph create -set_active true
sentinel register -set_active true -mode ir main.jir
walker run init 



actions load local main.py
// actions load local test.py
actions load local webhook/webhook_actions.py
jac build main.jac
sentinel register -set_active true -mode ir main.jir



walker run inter -ctx  "{\"path\" : \"ztest3.json\"}"


walker run vs_recognizer -ctx  "{\"image_data\" : \"database/Jolie/img1.jpeg\"}"
walker run vs_recognizer -ctx  "{\"image_data\" : \"database/Tharick/timg2.jpg\"}"
walker run interact -ctx  "{\"image_data\" : \"database/Tharick/timg2.jpg\", \"expression\" : \"SMILE\"}"
walker run interact -ctx  "{\"image_data\" : \"database/Tharick/timg2.jpg\", \"expression\" : \"sd\"}"


walker run get_webhook_url -ctx  "{\"token\" : \"b303f4f3a15e652ba6167161b071b8cb5cb2289c352992cd8f17708abadae59b\", \"url\" : \"http://0.0.0.0:8002\", \"proxy_url\" : \"https://8971-190-93-37-93.ngrok-free.app\", \"name\": \"interact\"}"

walker run get_webhook_url -ctx  "{\"token\" : \"2ef828b2935f311fdec9d6b1bed469e467dbf6b2b7538b63ee8f5320c8a47848\", \"url\" : \"http://0.0.0.0:8002\", \"proxy_url\" : \"https://0ece-190-93-37-191.ngrok-free.app\", \"name\": \"interact\"}"

*/

