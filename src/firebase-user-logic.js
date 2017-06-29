function get_database() {
    return window.database;
}

function get_user() {
    return window.user;
}

function get_current_uid() {
    return get_user().uid;
}

function get_value(key) {
    var value = null;
    var database = get_database();
    database.ref(key).once("value")
        .then(function(snapshot) {
            value = snapshot.val();
        });
    return value;
}

function set_value(key, value) {
    var database = get_database();
    database.ref(key).set(value);
}

function del_value(key) {
    var database = get_database();
    database.ref(key).remove();    
}

// FNV-1a hashing function chosen based on: 
// [stackexchange]/questions/49550/which-hashing-algorithm-is-best-for-uniqueness-and-speed
// Implementation copied from https://gist.github.com/vaiorabbit/5657561
// which was inferred from http://isthe.com/chongo/tech/comp/fnv/
//
// NOTE: This can support somewhere around 4 billion entries in theory,
//       but it is probably an order of magnitude or two lower than that.
//       Currently, this is only used to differentiate between endorsements
//       on a given user, so this should be okay (our choice of the 32-bit variant)
function idx_from_str(str) {
	var hval = 0x811c9dc5;
	for ( var i = 0; i < str.length; ++i )
	{
		hval ^= str.charCodeAt(i);
		hval += (hval << 1) + (hval << 4) + (hval << 7) + (hval << 8) + (hval << 24);
	}
	return '0x' + (hval >>> 0).toString(16); // Hex String
}

function process_datetime(timestamp) {
    // If no date provided, use now
    if (!timestamp)
        var timestamp = new Date();
    
    // Format is yyyy MMM (dd)
    // This format is used for searching by date
    var processed_datetime = timestamp.getFullYear() + ' ';
    // Provide full month names
    var monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ];
    processed_datetime += monthNames[timestamp.getMonth()];
    
    // Date is optional
    var dd = timestamp.getDate();
    if (dd) processed_datetime += ' ' + dd;
    
    return processed_datetime;
}

//Invite a new user (anonmyous account until sign-up?)
//TODO

// Anaylze and add skills to user
function get_skills(str) {
    skills = str.split(' ')
        .filter(function(word) {
            return word[0] = '#';
        })
        .map(function(word) { 
            word.substring(1); 
        });
    return skills;
}

// Logic to update user's skill multiplier
function update_skills(uid_to, endorsement) {
    var database = get_database();
    var skills = get_skills(endorsement['text']);
    var scores = skills.map(function(skill) {
            var v = get_value('skills/' + uid_to + '/' + skill);
            return v ? v : 0;
        });
    var uid_from = endorsement['from'];
    var multipliers = skills.map(function(skill) {
            var v = get_value('skills/' + uid_from + '/' + skill);
            return v ? v : 1;
        });
    for (var i = 0; i < skills.length; i++)
        set_value('skills/' + uid_to + '/' + skills[i], scores[i]+multipliers[i]);
}

function add_user(user) {
    if (get_value('users/' + user.uid) == null) {
        set_value('users/' + user.uid, { 
            name : user.displayName,
            email : user.email
        });
    }
}

function get_user_from_uid(uid) {
    return get_value('users/' + uid);
}

function get_user_relationships() {
    return get_value('relationships/' + get_current_uid());
}

//Get all pending endorsements waiting on current user
function get_pending() {
    return get_value('pending/' + get_current_uid());
}

//Get endorsements (sort by data)
function get_endorsements_by_user(uid) {
    return get_value('endorsements/' + uid);
}

//Add endorsement to another user
function add_endorsement(uid_to, endorsement_text, post_time) {
    var database = get_database();
    var uid_from = get_current_uid();
    var idx = idx_from_str(uid_from+endorsement_text);
    set_value('pending/' + uid_to + '/' + idx, {
        text: endorsement_text,
        from: uid_from,
        time: post_time,
        to: uid_to // This is used to keep track of the final
                   // approver, aka which user to move from 
                   // 'pending' to 'endorsements' under
    });
}

//Accept an endorsement
function accept_pending(idx) {
    var curr_uid = get_current_uid();
    // Get the endorsement we want to commit
    var endr = get_value('pending/' + curr_uid + '/' + idx);
    // Remove pending-only data
    uid_to = endr['to'];
    delete endr['to']; // No longer necessary to track who it's originally from
    
    // Commit to the public ledger of endorsements and remove it from pending
    // NOTE: An approved amendment (by either party) or an accepted original
    //       will move this from pending to permanent (public) endorsement
    set_value('endorsements/' + uid_to + '/' + idx, endr);
    del_value('pending/' + curr_uid + '/' + idx);
    // Update skills
    update_skills(uid_to, endr);
}

//Amend an endorsement
function amend_pending(idx, updated_text) {
    var curr_uid = get_current_uid();
    // Get the endorsement we want to commit
    var endr = get_value('pending/' + curr_uid + '/' + idx);
    endr['text'] = updated_text;
    
    // Toggle between who is approving to determine who gets it next
    uid_to = endr['to'];
    uid_from = endr['from'];
    next_uid = (curr_uid == uid_to) ? uid_from : uid_to;
    // Add to their queue
    set_value('pending/' + next_uid + '/' + idx, endr);
    // Remove from my queue
    del_value('pending/' + uid + '/' + idx);
}

//Reject an endorsement
function reject_pending(idx) {
    var uid = get_current_uid();
    // Completely remove from the database
    del_value('pending/' + uid + '/' + idx);
}
