// Function that allows the user to follow multiple users by clicking without visiting the profile
document.addEventListener('DOMContentLoaded', function () {

    if (document.getElementById("btnSuggestions")) {
        document.querySelectorAll('#btnSuggestions').forEach(e => e.addEventListener("click", function (event) {
            
            fetch(`/follow/${this.dataset.id}`)
                .then(response => response.json())
                .then(data => {
                    if (data.result == "follow") {
                        this.innerHTML = "Following";
                        var update = Number(document.getElementById('sp_following').innerHTML);
                        document.getElementById('sp_following').innerHTML = update + 1;



                        // Add the user to new following List

                var element = document.createElement("div");
                element.innerHTML = ` <div class="profilePic" data-identifier>
                <img id="followingProfile2" class="picture"  src="${data.user_profile}"></div>
                <div id="card" class="card">
                <div class="card-body">

                <h5 class="card-title"><a id="followingUser" href="/profile/${data.followinguser}">${data.followinguser}</a> <i class="fas fa-check-circle"></i></h5>
            
                 <p class="card-text">
                <div id="myBio" style="margin-right:7%;" class="card-link">&nbsp<small class="text-muted">${data.bio}</small>
                </div> </p></div>`;



                document.getElementById('content1').appendChild(element);





                    } else {
                        this.innerHTML = "Follow";
                        var update = Number(document.getElementById('sp_following').innerHTML);
                        document.getElementById('sp_following').innerHTML = update - 1;

                         var select = document.getElementById('content1');
                            select.removeChild(select.lastChild);


                    }

                    
                });

        }))
    }

    
  
});


