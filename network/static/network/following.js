// Window pops up, Shows who the user is following, when clicking on the number of followers
function showFollowing(){
    var lightbox = document.getElementById('followingJs'); // in layout.html
    lightbox.style.visibility = 'hidden';

    dimmer = document.createElement("div");
    dimmer.style.width =  window.innerWidth + 'px';
    dimmer.style.height = window.innerHeight + 'px';
    dimmer.className = 'dimmer';
    
    dimmer.onclick = function(){
        document.body.removeChild(this);   
        lightbox.style.visibility = 'hidden';
    }

    var x = document.getElementById('closeX');
    x.onclick = function(){
        dimmer.className = '';  
        lightbox.style.visibility = 'hidden';
    }

    document.body.appendChild(dimmer);
    
    lightbox.style.visibility = 'visible';
    return false;
}

// PopUp form for User's Followers
function showFollowers(){

    var lightbox = document.getElementById('followersJs');

    lightbox.style.visibility = 'hidden';

    dimmer = document.createElement("div");
    
    dimmer.style.width =  window.innerWidth + 'px';
    dimmer.style.height = window.innerHeight + 'px';
    dimmer.className = 'dimmer';
    
    dimmer.onclick = function(){
        document.body.removeChild(this);   
        lightbox.style.visibility = 'hidden';
    }



    document.body.appendChild(dimmer);

    var x = document.getElementById('closeX2');
    x.onclick = function(){
        dimmer.className = '';  
        lightbox.style.visibility = 'hidden';
    }
    lightbox.style.visibility = 'visible';
    return false;
}

