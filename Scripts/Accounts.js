//const { FileEnumerator } = require("eslint/use-at-your-own-risk");
//const { default: firebase } = require("firebase/compat/app");

const firebaseConfig = {
  apiKey: "AIzaSyBCOBG9DxKMA9pkWq1c-ANOAbKGHD4lPlg",
  authDomain: "coasteroperatorweb.firebaseapp.com",
  projectId: "coasteroperatorweb",
  storageBucket: "coasteroperatorweb.appspot.com",
  messagingSenderId: "828344346686",
  appId: "1:828344346686:web:d8a8ae2eadecb82f46896f",
  measurementId: "G-0THBL04QM8",
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);

const auth = firebase.auth();
const database = firebase.database();

function register() {
  // Get all input feilds
  email = document.getElementById("email").value
  password = document.getElementById("password").value
  username = document.getElementById("username").value
  firstname = document.getElementById("firstname").value
  lastname = document.getElementById("lastname").value

  // Validate input fields
  if (Validate_Email(email) == false || validate_password(password) == false) {
    alert('Email or password is not correct!')
    return
    // Dont keep running code
  }
  if (validate_field(firstname) == false || validate_field(lastname) == false || validate_field(username) == false) {
    alert('One of the input feilds are invalid')
    return
  }
  // Register user
  auth.createUserWithEmailAndPassword(email,password)
  .then(function() {

    var user = auth.currentUser
    alert('User created')

    // Declare user variable
    var user = auth.currentUser

    // Add user to database
    var database_ref = database.ref()

    // Create user data
    var user_data = {
      email : email,
      username : username,
      firstname : firstname,
      lastname : lastname,
      last_login : Date.now()
    }

    database_ref.child('users/' + user.uid ).set(user.data)

  })
  .catch(function(error) {
    // Firebase will use this to alert any errors
    var error_code = error.error_code
    var error_message = error.message

    alert(error_message)
  })
}

function Validate_Email(email) {
expression = /^[^@]+@\w+(\.\w+)+\w$/
if (expression.test(email) == true) {
  // Email is good
  return true
} else {
  // Email is bad
  return false
  }
}

function validate_password(password) {
  if (password < 6 ) {
    return false
  } else {
    return true
  }
}

function validate_field(feild) {
  if (feild == null) {
    return false
  }

  if (feild.length <= 0) {
    return false
  } else {
  return true
  }
}