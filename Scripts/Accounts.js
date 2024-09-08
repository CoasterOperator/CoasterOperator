const { default: firebase } = require("firebase/compat/app");

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

function register() {}
