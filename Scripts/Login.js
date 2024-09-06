

let users = [];

if (localStorage.getItem("users") != null) {
  users = JSON.parse(localStorage.getItem("users"));
}




function Login() {
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;

    if (username == "Admin" && password == "123") {
       return true
    }
}