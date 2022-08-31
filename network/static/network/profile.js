
// Pops up the Edit Profile section where the user can make changes.
function editProfile(){
    var profile = document.getElementById('ProfileImage');
    var lightbox = document.getElementById('profileEdit');

    lightbox.style.visibility = 'hidden';

    dimmer = document.createElement("div");
    dimmer.style.width =  window.innerWidth + 'px';
    dimmer.style.height = window.innerHeight + 'px';
    dimmer.className = 'dimmer';
    


    dimmer.onclick = function(){
        document.body.removeChild(this);   
        lightbox.style.visibility = 'hidden';
    profile.style.visibility = 'visible';


    }

    var x = document.getElementById('closeX3');
    x.onclick = function(){
        dimmer.className = '';  
        lightbox.style.visibility = 'hidden';
    profile.style.visibility = 'visible';


    }

    document.body.appendChild(dimmer);
    profile.style.visibility = 'hidden';
    lightbox.style.visibility = 'visible';
    return false;
}



function HideProfilePic(){
    var profile = document.getElementById('ProfileImage');
    profile.style.visibility = 'hidden';
}




function postsForm(){
     var profile = document.getElementById('ProfileImage');
    var lightbox = document.getElementById('popPostForm');

    lightbox.style.visibility = 'hidden';

    dimmer = document.createElement("div");
    dimmer.style.width =  window.innerWidth + 'px';
    dimmer.style.height = window.innerHeight + 'px';
    dimmer.className = 'dimmer';
    


    dimmer.onclick = function(){
        document.body.removeChild(this);   
        lightbox.style.visibility = 'hidden';
    profile.style.visibility = 'visible';


    }

    var x = document.getElementById('x22');
    x.onclick = function(){
        dimmer.className = '';  
        lightbox.style.visibility = 'hidden';
    profile.style.visibility = 'visible';


    }

    document.body.appendChild(dimmer);
    profile.style.visibility = 'hidden';
    lightbox.style.visibility = 'visible';
    return false;
}