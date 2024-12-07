import { initializeApp } from "firebase/app";
import {
  createUserWithEmailAndPassword,
  getAuth,
  sendEmailVerification,
  User,
} from "firebase/auth";
import firebaseConfig from "./firebase-config.json" with { type: "json" };

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

const sendVerifyEmail = async (user: User) => {
  try {
    await sendEmailVerification(user);
    console.log("Email verification sent!");
  } catch (error) {
    console.error(error);
  }
};

const createUser = async (email: string, password: string) => {
  try {
    const userCredential = await createUserWithEmailAndPassword(
      auth,
      email,
      password,
    );
    const user = userCredential.user;
    console.log(user);
    await sendVerifyEmail(user);
  } catch (error) {
    console.error(error);
  }
};

const email = Deno.env.get("EMAIL");
const password = Deno.env.get("PASSWORD");

if (!email || !password) {
  console.error("Please provide email and password");
  Deno.exit(1);
}

createUser(email, password);
