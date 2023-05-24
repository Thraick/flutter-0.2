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
    has image_data = {};
    has expression;
    
    if (image_data){
        id = spawn net.root() walker::vs_recognizer(image_data=image_data);
    }

    expression_list = ["HAPPY","SAD","ANGRY","SUPRISE","FEAR","DISGUST"];

    if(expression and expression not in expression_list){
        report:custom = {"ERROR": "Expression '"+expression+"'is not in " + expression_list.str};
        report:status = 404;
    }
    else: report expression;
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
actions load local test.py
actions load local webhook/webhook_actions.py
jac build main.jac
sentinel register -set_active true -mode ir main.jir



walker run vs_recognizer -ctx  "{\"image_data\" : \"database/Jolie/img1.jpeg\"}"
walker run vs_recognizer -ctx  "{\"image_data\" : \"database/Tharick/timg2.jpg\"}"
walker run interact -ctx  "{\"image_data\" : \"database/Tharick/timg2.jpg\", \"expression\" : \"SMILE\"}"
walker run interact -ctx  "{\"image_data\" : \"database/Tharick/timg2.jpg\", \"expression\" : \"sd\"}"


walker run get_webhook_url -ctx  "{\"token\" : \"6f20aa57cc2ada063004e8b13737c398a69cd20b5fb0b856eebd033229474833\", \"url\" : \"http://0.0.0.0:8002\", \"proxy_url\" : \"https://a56e-190-93-37-193.ngrok-free.app\", \"name\": \"interact\"}"



*/

