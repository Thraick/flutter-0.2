walker vs_recognizer {
    has image_data;
    has anchor identity;

    can cv.encode_face, cv.compare_face_encodings;
    #the encode_face takes an image of a face and returns facial landmark / encoding of that face
    #the compare_face_encodings takes two encodings o f facial landmark data and returns a similarity factor
    face_encoding =  cv.encode_face(image_data);
    if (face_encoding == []){
        report:status = 400;
        report "No encoding found";
        disengage; 
    }
    else {
        identities = spawn net.root() walker::list_identities;
        if (!identities['encodings']){
            std.out("create1");
            identity = spawn net.root() walker::create_identity(encodings = face_encoding);
        }else{
            std.out("compare");
            identity = cv.compare_face_encodings(identities['encodings'], identities['id'], face_encoding);
        }
        if (!identity){
            std.out("create2");
            identity = spawn net.root() walker::create_identity(encodings = face_encoding);
        }
        report identity;
    }
}




// creates an identity
walker create_identity {

    has encodings;
    has anchor id;

    root: take --> node::app_root;
    app_root: take --> node::identities;
    identities {
        nd = spawn here ++> node::identity(encodings = encodings);
        nd.id = nd.info['jid'];
        id = nd.info['jid'];
        // report nd;
        disengage;
    }
}

// updates a created identity; 
// nd must be specified along with optional params in the ctx param
walker update_identity {
    
    has encodings;

    identity {
        if(encodings): here.encodings = encodings;
        report here;
        disengage;
    }
}

// deletes identity node; node jid must be specified in nd param
walker delete_identity {
    identity {
        report here;
        destroy here;
        disengage;
    }
}

// returns identity node; node jid must be specified in nd param
walker get_identity {
    identity {
        report here;
        disengage;
    }
}

// returns list of identities
walker list_identities {
    has anchor data = {};

    root: take --> node::app_root;
    app_root: take --> node::identities;
    identities{
        data['encodings']= -->.encodings;
        data['id']= -->.id;
        // ww = -->.encodings;

        // if (ww){
        //     data['encodings']= ww;
        //     data['id']= -->.id;
        // }
        // report data;
    }
}