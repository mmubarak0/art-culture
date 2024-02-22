var login = () => {
    window.location.assign("./login.html");
};

const FirstName = document.getElementById("fristname");
const LastName = document.getElementById("lastname");
const Email = document.getElementById("email");
const MobileNumber = document.getElementById("mobilenumber");
const Password = document.getElementById("password");
const ReEnterPassword = document.getElementById("Repassword");
const message = document.getElementById("message");
var regex = /^[\w\-\.\+]+\@[a-zA-Z0-9\. \-]+\.[a-zA-z0-9]{2,4}$/;

const SignUp = () => {
    if (FirstName.value === "") {
      message.innerHTML = "First Name Required!";
      message.style.color = "red";
    } else if (LastName.value === "") {
      message.innerHTML = "Last Name Required!";
      message.style.color = "red";
    } else if (MobileNumber.value === "") {
      message.innerHTML = "Mobile Number Required!";
      message.style.color = "red";
    } else if (MobileNumber.value.length < 11) {
      message.innerHTML = "Please Enter 11 digit Mobile No.";
      message.style.color = "red";
    } else if (Email.value === "") {
      message.innerHTML = "Email Address Required!";
      message.style.color = "red";
    } else if (!Email.value.match(regex)) {
      message.innerHTML = "Please Enter Correct Email Address";
      message.style.color = "red";
    } else if (Password.value === "") {
      message.innerHTML = "Password Required";
      message.style.color = "red";
    } else if (Password.value.length < 6) {
      message.innerHTML = "Please Enter at least 6 digit Password";
      message.style.color = "red";
    } else if (ReEnterPassword.value === "") {
      message.innerHTML = "Re Enter Password Required";
      message.style.color = "red";
    } else if (ReEnterPassword.value !== Password.value) {
      message.innerHTML = "Password donot match";
      message.style.color = "red";
    }else{
      firebase.auth().createUserWithEmailAndPassword( Email.value, Password.value)
  .then((userCredential) => {
    var d = new Date().toLocaleDateString();
    // database
    var userdata = {
      FirstName: FirstName.value,
      LastName: LastName.value,
      MobileNumber: MobileNumber.value,
      Email: Email.value,
      Password: Password.value,
      ReEnterPassword: ReEnterPassword.value,
      uid: userCredential.user.uid,
      ProfilePicture: "",
      CoverPicture: "",
      Description: "",
      Signupdate: `${d}`,
    };
    firebase.firestore().collection("users").doc(userCredential.user.uid).set(userdata).then((res)=>{
      message.innerHTML ="Account was created successfuly"
      message.style.color ="green"
      const user = firebase.auth().currentUser;
      user.sendEmailVerification().then((res)=>{
        setTimeout(()=>{
          window.location.assign("../pages/emailVerifiaction.html")
        },2000)
      })
    })
    message.innerHTML= "Sign Up Successfully"
  })
  .catch((error) => {
    message.innerHTML = error.message;
    // ..
  });
        
    }
}