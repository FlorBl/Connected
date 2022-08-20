

                let user = 'zumba';
                fetch(`/jsonresponse/profile=${user}`)
                .then(response => response.json())
                .then(data => { console.log(data);
                const userInfo = data['UsersInfo'];


                var user,picture;
                // Method One
                for (let i = 0; i < data['UsersInfo'].length; i++) {

                
                id = data['UsersInfo'][i].id;
                bio = data['UsersInfo'][i].bio;
                user = data['UsersInfo'][i].username;
                picture = data['UsersInfo'][i].profile_image;

                const aws3 = 'https://django-greensky-bucket.s3.amazonaws.com/'
                var profileImage = `${aws3}`+`${picture}`;

                var element = document.createElement("div");
                
                element.innerHTML = ` <div class="profilePic">
                <img id="followingProfile2" class="picture"  src="${profileImage}"></div>
                <div id="card" class="card">
                <div class="card-body">

                <h5 class="card-title"><a id="followingUser" href="/profile/${user}">${user}</a> <i class="fas fa-check-circle"></i></h5>


                 <p class="card-text">
                <div id="myBio" style="margin-right:7%;" class="card-link">&nbsp<small class="text-muted">${bio}</small>
                </div> </p></div>`;

                

                document.getElementById('content1').appendChild(element);




                }




                // Method Two
                for (const user of userInfo){
                    //console.log(user);

                }


                
                });



