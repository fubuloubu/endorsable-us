function get_database() {
    return window.database;
}

function get_user() {
    return window.user;
}

//Get endorsements (sort by data)
function get_endorsements_by_user(user) {
    var database = get_database();
    var results = {};
    if (database.ref('endorsements/' + user.id))
        results =
        database.ref('endorsements/' + user.id);
    return results
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

//Add endorsement to another user
function add_endorsement(user_to, endorsement_text, post_time) {
    var database = get_database();
    var user_from = get_user();
    var idx = idx_from_str(user_from.id+endorsement_text);
    database.ref('pending/' + user_to.uid + '/' + idx).set({
        text: endorsement_text,
        from: user_from.uid,
        time: post_time,
        finalized: true
    });
}

//Get all pending endorsements
function get_pending() {
    var database = get_database();
    var user = get_user();
    var results = {};
    if (database.ref('pending/' + user))
        results =
        database.ref('pending/' + user);
    return results
}

// Anaylze and add skills to user
function get_skills(str) {
    skills = str.split(' ').filter(function(word) {
        return word[0] = '#';
    });
    return skills;
}
function update_skills(user, endorsement) {
    var database = get_database();
    var skills = get_skills(endorsement['text']);
    var scores = skills.map(function(skill) {
        var v = database.ref('skills/' + user.uid + '/' + skill);
        return v ? v : 0;
    });
    var user_from = endorsement['from'];
    var multipliers = skills.map(function(skill) {
        var v = database.ref('skills/' + user_from.uid + '/' + skill);
        return v ? v : 1;
    });
    for (var i = 0; i < skills.length; i++)
        database.ref('skills/' + user.uid + '/' + skills[i]).set(scores[i]+multipliers[i]);
}

//Accept and endorsement
function accept_pending(idx) {
    var database = get_database();
    var user = get_user();
    // Get the endorsement we want to commit
    var endr = database.ref('pending/' + user.uid + '/' + idx);
    // Remove pending-only data
    delete endr['finalized'];
    // Commit to the public ledger of endorsements and remove it from pending
    database.ref('endorsements/' + user.uid + '/' + idx).set(endr);
    database.ref('pending/' + user.uid + '/' + idx).remove();
    // Update skills
    update_skills(user, endr);
}

//Amend an endorsement
function amend_pending(idx, updated_text) {
    var database = get_database();
    var user = get_user();
    // Get the endorsement we want to commit
    var endr = database.ref('pending/' + user.uid + '/' + idx);
    // Rem
    endr['finalized'] = false;
    endr['text'] = updated_text;
    // Commit to the public ledger of endorsements and remove it from pending
    database.ref('pending/' + user.uid + '/' + idx).set(endr);
}

//Approve an amendment
function approve_pending(user_to, idx) {
    var database = get_database();
    // Get the endorsement we want to commit
    var endr = database.ref('pending/' + user_to.uid + '/' + idx);
    // Remove pending-only data
    delete endr['finalized'];
    // Commit to the public ledger of endorsements and remove it from pending
    database.ref('endorsements/' + user_to.uid + '/' + idx).set(endr);
    database.ref('pending/' + user_to.uid + '/' + idx).remove();
    // Update skills
    update_skills(user_to, endr);
}

//Reject an endorsement
function reject_pending(idx) {
    var database = get_database();
    var user = get_user();
    // Get the endorsement we want to commit
    database.ref('pending/' + user.uid + '/' + idx).remove();
}
