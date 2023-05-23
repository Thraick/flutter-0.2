import {*} with "graph.jac";
import {*} with "./identities/identities_walkers.jac";
import {*} with "./webhook/webhook_walkers.jac";

walker init {

    root {
        take --> node::app_root else { 
            spawn here ++> graph::app_graph; }
    }
}

// walker vs_recognizer: anyone {
//     has image_data;
//     has anchor identity;

//     report image_data;
// }




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
actions load local webhook/webhook_actions.py
jac build main.jac
sentinel register -set_active true -mode ir main.jir



walker run vs_recognizer -ctx  "{\"image_data\" : \"database/Jolie/img1.jpeg\"}"
walker run vs_recognizer -ctx  "{\"image_data\" : \"database/Tharick/timg2.jpg\"}"


walker run get_webhook_url -ctx  "{\"token\" : \"681abcae51894ac84558c653954f1d887ba6f3e9dd5b0395c44ddd178deea3ef\", \"url\" : \"http://0.0.0.0:8002\", \"proxy_url\" : \"https://e00f-190-93-37-193.ngrok-free.app\", \"name\": \"vs_recognizer\"}"



*/

