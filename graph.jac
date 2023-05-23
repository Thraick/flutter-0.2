import {*} with "./identities/identities_graph.jac";

node app_root;

graph app_graph {

    has anchor app_root;

    spawn {
        app_root = spawn node::app_root;
        identities = spawn app_root ++> node::identities;
    }

}
