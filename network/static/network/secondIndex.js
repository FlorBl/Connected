
// Register/Login Form Popup after logging out
function registerIndex(){

    var lightbox = document.getElementById('registerIndex');

    lightbox.style.visibility = 'hidden';

    dimmer = document.createElement("div");
    
    dimmer.style.width =  window.innerWidth + 'px';
    dimmer.style.height = window.innerHeight + 'px';
    dimmer.className = 'dimmer';
    
    dimmer.onclick = function(){
        document.body.removeChild(this);   
        lightbox.style.visibility = 'hidden';
    }

    var x = document.getElementById('closeX3');
    x.onclick = function(){
        dimmer.className = '';  
        lightbox.style.visibility = 'hidden';
    }

    document.body.appendChild(dimmer);
    
    lightbox.style.visibility = 'visible';
    return false;
}


// Register Form Popup
function loginIndex(){

    var lightbox = document.getElementById('loginIndex');

    lightbox.style.visibility = 'hidden';

    dimmer = document.createElement("div");
    
    dimmer.style.width =  window.innerWidth + 'px';
    dimmer.style.height = window.innerHeight + 'px';
    dimmer.className = 'dimmer';
    
    dimmer.onclick = function(){
        document.body.removeChild(this);   
        lightbox.style.visibility = 'hidden';
    }

    var x = document.getElementById('closeX4');
    x.onclick = function(){
        dimmer.className = '';  
        lightbox.style.visibility = 'hidden';
    }

    document.body.appendChild(dimmer);
    
    lightbox.style.visibility = 'visible';
    return false;
}


