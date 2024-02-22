firebase.auth().onAuthStateChanged((user) => {
    if (user) {
      if (user.emailVerified) {
        // home
        setTimeout(() => {
          window.location.assign("./pages/home.html");
        }, 1000);
      } else {
        // email verification
        setTimeout(() => {
          window.location.assign("./pages/email.html");
        }, 1000);
      }
    } else {
      // login
      setTimeout(() => {
        window.location.assign("./pages/login.html");
      }, 1000);
    }
  });
  