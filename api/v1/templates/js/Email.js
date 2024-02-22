let email = document.getElementById("emailid");
let message = document.getElementById("message");
firebase.auth().onAuthStateChanged((user) => {
  if (user) {
    console.log(user);
    if (user.emailVerified) {
      window.location.assign("../pages/home.html");
    } else {
      email.innerHTML = user.email;
    }
  } else {
    window.location.assign("./login.html");
  }
});
let resend = () => {
  firebase
    .auth()
    .currentUser.sendEmailVerification()
    .then(() => {
      message.innerHTML =
        "A verification link has been send to your email account";
      message.style.color = "green";
      message.style.marginBottom = "15px";
    });
};
let reloud = () => {
  location.reload();
};