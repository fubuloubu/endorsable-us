// If user is not in system, add them!
function add_user() {
    var user_ref = window.database.ref('users/' + window.user.uid);
    if (!user_ref) {
        user_ref.set({
            name: window.user.displayName,
            photo: window.user.photoURL,
        });
    }
}

function get_user() {
    return window.user;
}

//Invite a new user (anonmyous?)
//Add endorsement to another user
//Accept and endorsement
//Amend an endorsement
//Reject an endorsement

//Get endorsements (with the given filter)
//Get skills (with the given filter)
