let userprofileimg = document.getElementById("userprofileimg");
let usercoverimg = document.getElementById("usercoverimg");
let progressbar1 = document.getElementById("progressbar");
let progressbardiv = document.getElementById("progressbardiv");
let firstName = document.getElementById("firstname");
let lastname = document.getElementById("lastname");
let mobilenumber = document.getElementById("mobileno");
let email = document.getElementById("emailaddress");
let description = document.getElementById("userdescription");
let message = document.getElementById("message");
var postsshowbutton = document.getElementById("postsbutton");
var currentuserpost = document.getElementById("showposts");
var userdata = document.getElementById("editabledatadiv");
var showuserprofilebutton = document.getElementById("userprofilebutton");
let textareaupdate = document.getElementById("textareaupdate");
let fileType = "";
let uid;
let updateurl;
let alluser = [];
let allposts = [];
// changecoverpicture
function changecoverpicture(event) {
  var uploadTask = firebase
    .storage()
    .ref()
    .child(`users/${uid}/coverpicture`)
    .put(event.target.files[0]);
  uploadTask.on(
    "state_changed",
    (snapshot) => {
      var progress = (snapshot.bytesTransferred / snapshot.totalBytes) * 100;
      progressbardiv.style.visibility = "visible";
      var uploadpercentage = Math.round(progress);
      progressbar.style.width = `${uploadpercentage}%`;
      progressbar.innerHTML = `${uploadpercentage}%`;
    },
    (error) => {},
    () => {
      uploadTask.snapshot.ref.getDownloadURL().then((coverpicture) => {
        progressbardiv.style.visibility = "hidden";
        firebase
          .firestore()
          .collection("users/")
          .doc(uid)
          .update({ CoverPicture: coverpicture });
      });
    }
  );
}

// changeprofilepicture
function changeprofilepicture(event) {
  var uploadTask = firebase
    .storage()
    .ref()
    .child(`users/${uid}/profilepicture`)
    .put(event.target.files[0]);
  uploadTask.on(
    "state_changed",
    (snapshot) => {
      var progress = (snapshot.bytesTransferred / snapshot.totalBytes) * 100;
      progressbardiv.style.visibility = "visible";
      var uploadpercentage = Math.round(progress);
      progressbar1.style.width = `${uploadpercentage}%`;
      progressbar1.innerHTML = `${uploadpercentage}%`;
    },
    (error) => {},
    () => {
      uploadTask.snapshot.ref.getDownloadURL().then((profileimage) => {
        progressbardiv.style.visibility = "hidden";
        firebase
          .firestore()
          .collection("users/")
          .doc(uid)
          .update({ ProfilePicture: profileimage });
      });
    }
  );
}

firebase.auth().onAuthStateChanged((user) => {
  if (user) {
    if (user.emailVerified) {
      uid = user.uid;
      // console.log("emailVerified true");
      var createpostinput = document.getElementById("a");
      firebase
        .firestore()
        .collection("users")
        .onSnapshot((result) => {
          result.forEach((users) => {
            alluser.push(users.data());
            fileType = users.data().filetype;
            if (users.data().uid === user.uid) {
              createpostinput.setAttribute(
                "placeholder",
                `What's on your mind ,${users.data().FirstName}?`
              );
              firstName.value = users.data().FirstName;
              lastname.value = users.data().LastName;
              mobilenumber.value = users.data().MobileNumber;
              email.value = users.data().Email;
              email.disabled = true;
              description.value = users.data().Description;

              if (users.data().ProfilePicture !== "") {
                userimg.setAttribute("src", users.data().ProfilePicture);
              }
            }
          });
        });

      firebase
        .firestore()
        .collection("users/")
        .onSnapshot((result) => {
          result.forEach((users) => {
            alluser.push(users.data());
            Filetype = users.data().filetype;
            if (users.data().uid === user.uid) {
              if (
                users.data().ProfilePicture !== "" ||
                users.data().CoverPicture !== ""
              ) {
                userprofileimg.setAttribute(
                  "src",
                  users.data().ProfilePicture || "https://cdn.pixabay.com/photo/2015/03/04/22/35/avatar-659651__340.png"
                );
                usercoverimg.setAttribute(
                  "src",
                  users.data().CoverPicture ||
                    "https://media.istockphoto.com/id/490726872/photo/man-at-the-sunrise.jpg?b=1&s=170667a&w=0&k=20&c=ftoG5oljywajspsDYs9N37LgtiYYRHyySxgGpQb9r0Y="
                );
              }
            }
          });
        });
    } else {
      window.location.assign("./email.html");
    }
  } else {
    window.location.assign("./login.html");
  }
});
postsshowbutton.addEventListener("click", () => {
  userdata.style.display = "none";
  currentuserpost.style.display = "block";
  postsshowbutton.style.backgroundColor = "#0000ff";
  postsshowbutton.style.color = "white";
  showuserprofilebutton.style.backgroundColor = "white";
  showuserprofilebutton.style.color = "#0000ff";
  document.getElementById("currentuserpostsdiv").style.display = "flex";
});
showuserprofilebutton.addEventListener("click", () => {
  userdata.style.display = "block";
  currentuserpost.style.display = "none";
  showuserprofilebutton.style.backgroundColor = "#0000ff";
  showuserprofilebutton.style.color = "white";
  postsshowbutton.style.backgroundColor = "white";
  postsshowbutton.style.color = "#0000ff";
  document.getElementById("currentuserpostsdiv").style.display = "none";
});

// update button
let update = () => {
  if (firstName.value === "") {
    message.innerHTML = "First Name Required";
    message.style.color = "red";
    firstName.focus();
  } else if (lastname.value === "") {
    message.innerHTML = "Last Name Required";
    message.style.color = "red";
    lastname.focus();
  } else if (mobilenumber.value === "") {
    message.innerHTML = "Mobile Number Required";
    message.style.color = "red";
    mobilenumber.focus();
  } else {
    var data = {
      firstName: firstName.value,
      lastName: lastname.value,
      mobileNumber: mobilenumber.value,
      Description: description.value
    };
    console.log(data);
    firebase
      .firestore()
      .collection("users")
      .doc(uid)
      .update(data)
      .then((res) => {
        console.log(res);
        message.innerHTML = "Successfully Updated";
        message.style.color = "green";
        setTimeout(() => {
          message.innerHTML = "";
        }, 3000);
      })
      .catch((error) => {
        console.log(error);
      });
  }
};

// user posts
var loading = document.getElementById("loaderdiv");
var showposts = document.getElementById("showposts");
firebase
  .firestore()
  .collection("posts")
  .onSnapshot((onSnapshot) => {
    firebase
      .firestore()
      .collection("posts")
      .where("uid", "==", uid)
      .get()
      .then((onSnapshot) => {
        console.log(onSnapshot);
        loading.style.display = "none";
        let allposts = [];
        if (onSnapshot.size === 0) {
          let nodata = document.getElementById("messagediv");
          nodata.style.display = "block";
        } else {
          onSnapshot.forEach((postres) => {
            allposts.push(postres.data());
          });
          showposts.style.display = "block";
          showposts.innerHTML = "";
          for (let i = 0; i < allposts.length; i++) {
            let likearry = allposts[i].like;
            let dislikearry = allposts[i].dislikes;
            let commentarry = allposts[i].comments;
            let postmain = document.createElement("div");
            showposts.appendChild(postmain);
            postmain.setAttribute("class", "postmain");
            //post header
            let postheader = document.createElement("div");
            postmain.appendChild(postheader);
            postheader.setAttribute("class", "postheader");
            // user data
            firebase
              .firestore()
              .collection("users")
              .doc(allposts[i].uid)
              .get()
              .then((res) => {
                let userprodiv = document.createElement("div");
                let userprofileimage = document.createElement("img");
                postheader.appendChild(userprodiv);
                userprodiv.setAttribute("class", "userprodiv");
                userprodiv.appendChild(userprofileimage);
                userprofileimage.setAttribute(
                  "src",
                  res.data().ProfilePicture === ""
                    ? "https://cdn.pixabay.com/photo/2015/03/04/22/35/avatar-659651__340.png"
                    : res.data().ProfilePicture
                );
                userprofileimage.setAttribute("class", "profileimage");
                let userdiv = document.createElement("div");
                userprodiv.appendChild(userdiv);
                userdiv.setAttribute("class", "col-6");
                let = username = document.createElement("h6");
                userdiv.appendChild(username);
                username.innerHTML = `${res.data().FirstName} ${
                  res.data().LastName
                }`;

                let = date = document.createElement("h6");
                userdiv.appendChild(date);
                date.innerHTML = `${allposts[i].Date} `;
                let postdetail = document.createElement("p");
                postheader.appendChild(postdetail);

                var editanddeltebtndiv = document.createElement("div");
                userprodiv.appendChild(editanddeltebtndiv);
                editanddeltebtndiv.setAttribute(
                  "class",
                  "editanddeletbtn col-4"
                );

                var editbtn = document.createElement("i");
                editanddeltebtndiv.appendChild(editbtn);
                editbtn.setAttribute("class", "fa-solid fa-pencil postsbtn");
                editbtn.setAttribute("id", "editbtn");

                // edit button
                editbtn.addEventListener("click", () => {
                  showposts.style.display = "none";
                  let maincreate = document.getElementById("maincreate");
                  let user = document.getElementById("userdiv");
                  let userprodiv = document.createElement("div");
                  let userprofileimage = document.createElement("img");
                  user.appendChild(userprodiv);
                  userprodiv.setAttribute("class", "userprodiv");
                  userprodiv.appendChild(userprofileimage);
                  userprofileimage.setAttribute(
                    "src",
                    res.data().ProfilePicture === ""
                      ? "https://cdn.pixabay.com/photo/2015/03/04/22/35/avatar-659651__340.png"
                      : res.data().ProfilePicture
                  );
                  userprofileimage.setAttribute("class", "profileimage");
                  let userdiv = document.createElement("div");
                  userprodiv.appendChild(userdiv);
                  userdiv.setAttribute("class", "col-6");
                  let = username = document.createElement("h6");
                  userdiv.appendChild(username);
                  username.innerHTML = `${res.data().FirstName} ${
                    res.data().LastName
                  }`;
                  let = date = document.createElement("h6");
                  userdiv.appendChild(date);
                  date.innerHTML = `${allposts[i].Date} `;
                  let postdetail = document.createElement("p");
                  postheader.appendChild(postdetail);
                  maincreate.style.display = "block";
                  textareaupdate.innerHTML = allposts[i].postvalue;

                  
                let updatepostbtn = document.getElementById("updatepostbtn");
                updatepostbtn.addEventListener("click", () => {
                  var aa = {
                    postvalue: textareaupdate.value,
                    url: updateurl ||"",
                    filetype: fileType||""
                  };
                  firebase
                    .firestore()
                    .collection("posts")
                    .doc(allposts[i].id)
                    .update(aa)
                    .then(() => {
                      maincreate.style.display = "none";
                      showposts.style.display = "block";
                    });
                });
                });

                var deletbtn = document.createElement("i");
                editanddeltebtndiv.appendChild(deletbtn);
                deletbtn.setAttribute("class", "fa-solid fa-trash postsbtn");
                deletbtn.setAttribute("id", "deletebtn");
                deletbtn.style.marginLeft = "8px";

                // dlete button
                deletbtn.addEventListener("click", () => {
                  swal({
                    title: "Are you sure?",
                    text: "Once deleted, you will not be able to recover this Post !",
                    icon: "warning",
                    buttons: true,
                    dangerMode: true
                  }).then((willDelete) => {
                    if (willDelete) {
                      swal("Poof! Your imaginary file has been deleted!", {
                        icon: "success"
                      });
                      firebase
                        .firestore()
                        .collection("posts")
                        .doc(allposts[i].id)
                        .delete();
                      //Message
                    } else {
                      swal("Your imaginary file is safe!");
                    }
                  });
                });

                postdetail.innerHTML = allposts[i].postvalue;
                if (allposts[i].url !== "") {
                  if (
                    allposts[i].filetype === "image/png" ||
                    allposts[i].filetype === "image/jpeg" ||
                    allposts[i].filetype === "image/jpg"
                  ) {
                    // images
                    let postimage = document.createElement("img");
                    postmain.appendChild(postimage);
                    postimage.setAttribute("src", "");
                    postimage.setAttribute("src", allposts[i].url);
                    postimage.setAttribute("class", "postimage col-12");
                  } else {
                    // videos
                    let postvideo = document.createElement("video");
                    postmain.appendChild(postvideo);
                    postvideo.setAttribute("controls", "true");
                    postvideo.setAttribute("class", "postVideo");
                    let source = document.createElement("source");
                    postvideo.appendChild(source);
                    source.setAttribute("src", allposts[i].url);
                    source.setAttribute("type", "video/mp4");
                  }
                }

                // footer
                let footerdiv = document.createElement("div");
                postmain.appendChild(footerdiv);
                footerdiv.setAttribute("class", "footerdiv");
                //like
                var likebutton = document.createElement("button");
                footerdiv.appendChild(likebutton);
                likebutton.setAttribute("class", "likebutton");

                //like icon 
                var likeicon = document.createElement("i");
                likebutton.appendChild(likeicon);
                likeicon.setAttribute("class", "fa-solid fa-thumbs-up");

                var liketitle = document.createElement("p");
                likebutton.appendChild(liketitle);
                liketitle.setAttribute("class", "impressionstitle");
                liketitle.innerHTML = `Like (${likearry.length})`;
                for (
                  let likeIndex = 0;
                  likeIndex < likearry.length;
                  likeIndex++
                ) {
                  if (likearry[likeIndex] === uid) {
                    likeicon.style.color = "blue";
                    liketitle.style.color = "blue";
                  }
                }
                //like function
                likebutton.addEventListener("click", () => {
                  let like = false;
                  for (
                    let likeIndex = 0;
                    likeIndex < likearry.length;
                    likeIndex++
                  ) {
                    if (likearry[likeIndex] === uid) {
                      like = true;
                      likearry.splice(likeIndex, 1);
                    }
                  }
                  if (!like) {
                    likearry.push(uid);
                  }
                  firebase
                    .firestore()
                    .collection("posts/")
                    .doc(allposts[i].id)
                    .update({
                      like: likearry
                    });
                });

                var dislikebutton = document.createElement("button");
                footerdiv.appendChild(dislikebutton);
                dislikebutton.setAttribute("class", "dislikebutton");

                var dislikeicon = document.createElement("i");
                dislikebutton.appendChild(dislikeicon);
                dislikeicon.setAttribute("class", "fa-solid fa-thumbs-down");

                var disliketitle = document.createElement("p");
                dislikebutton.appendChild(disliketitle);
                disliketitle.setAttribute("class", "impressionstitle");
                disliketitle.innerHTML = `Dislike (${dislikearry.length})`;
                for (
                  let dislikeindex = 0;
                  dislikeindex < dislikearry.length;
                  dislikeindex++
                ) {
                  if (dislikearry[dislikeindex] === uid) {
                    dislikeicon.style.color = "blue";
                    disliketitle.style.color = "blue";
                  }
                }
                dislikebutton.addEventListener("click", () => {
                  let dislike = false;
                  for (
                    let dislikeindex = 0;
                    dislikeindex < dislikearry.length;
                    dislikeindex++
                  ) {
                    if (dislikearry[dislikeindex] === uid) {
                      dislike = true;
                      dislikearry.splice(dislikeindex, 1);
                    }
                  }
                  if (!dislike) {
                    dislikearry.push(uid);
                  }
                  firebase
                    .firestore()
                    .collection("posts/")
                    .doc(allposts[i].id)
                    .update({
                      dislikes: dislikearry
                    });
                });

                let commentbutton = document.createElement("button");
                footerdiv.appendChild(commentbutton);

                var commenticon = document.createElement("i");
                commentbutton.appendChild(commenticon);
                commenticon.setAttribute("class", "fa-solid fa-message");

                var commentmessage = document.createElement("p");
                commentbutton.appendChild(commentmessage);
                commentmessage.setAttribute("class", "impressionstitle");
                commentmessage.innerHTML = `Comment (${commentarry.length})`;
                // comment fuction
                if (commentarry.length !== 0) {
                  for (
                    var commentindex = 0;
                    commentindex < commentarry.length;
                    commentindex++
                  ) {
                    let commentmain = document.createElement("div");
                    postmain.appendChild(commentmain);
                    commentmain.setAttribute("class", "commentmain");
                    let commentprofileimage = document.createElement("img");
                    commentmain.appendChild(commentprofileimage);
                    commentprofileimage.setAttribute(
                      "class",
                      "commentprofileimage"
                    );
                    var commentmessage = document.createElement("div");
                    let commentusername = document.createElement("h6");
                    commentmain.appendChild(commentmessage);
                    commentmessage.appendChild(commentusername);
                    //user data
                    firebase
                      .firestore()
                      .collection("users")
                      .doc(commentarry[commentindex].uid)
                      .get()
                      .then((currentuserres) => {
                        commentprofileimage.setAttribute(
                          "src",
                          "https://cdn.pixabay.com/photo/2015/03/04/22/35/avatar-659651__340.png"
                        );
                        if (currentuserres.data().ProfilePicture !== "") {
                          commentprofileimage.setAttribute(
                            "src",
                            currentuserres.data().ProfilePicture
                          );
                        }
                        commentusername.innerHTML = `${
                          currentuserres.data().firstName
                        } ${currentuserres.data().lastName}`;
                      });
                    let commentvalue = document.createElement("p");
                    commentmessage.appendChild(commentvalue);
                    commentvalue.innerHTML =
                      commentarry[commentindex].commentvalue;
                  }
                }
                let writecomment = document.createElement("div");
                writecomment.setAttribute("class", "writecomment");
                postmain.appendChild(writecomment);
                let commentinput = document.createElement("input");
                writecomment.appendChild(commentinput);
                commentinput.setAttribute("class", "commentinput");
                commentinput.setAttribute("placeholder", "Write Comment.....");
                let sendbutton = document.createElement("img");
                writecomment.appendChild(sendbutton);
                sendbutton.setAttribute("src", "https://cdn-icons-png.flaticon.com/512/3682/3682321.png");
                sendbutton.setAttribute("class", "sendbutton");

                //comment fuction
                sendbutton.addEventListener("click", () => {
                  if (commentinput.value === "") {
                    alert("Please write something.....!");
                  } else {
                    let commentdata = {
                      commentvalue: commentinput.value,
                      uid: uid
                    };
                    commentarry.push(commentdata);
                    firebase
                      .firestore()
                      .collection("posts")
                      .doc(allposts[i].id)
                      .update({
                        comments: commentarry
                      });
                  }
                });
              });
          }
        }
      });
  });

let postfiles = (event) => {
  fileType = event.target.files[0].type;
  let progressdiv1 = document.getElementById("progressdiv1");
  let progressbar1 = document.getElementById("progressbar1");
  var uploadTask = firebase
    .storage()
    .ref()
    .child(event.target.files[0].name)
    .put(event.target.files[0]);
  uploadTask.on(
    "state_changed",
    (snapshot) => {
      var progress = (snapshot.bytesTransferred / snapshot.totalBytes) * 100;
      var uploadpercentage = Math.round(progress);
      console.log(uploadpercentage);
      progressdiv1.style.display = "block";
      progressbar1.style.width = `${uploadpercentage}%`;
      progressbar1.innerHTML = `${uploadpercentage}%`;
    },
    (error) => {},
    () => {
      uploadTask.snapshot.ref.getDownloadURL().then((downloadURL) => {
        console.log("File available at", downloadURL);
        updateurl = downloadURL;
        progressdiv1.style.display = "none";
      });
    }
  );
};
const logout = () => {
  firebase
    .auth()
    .signOut()
    .then(() => {
      window.location.assign("./login.html");
    });
};