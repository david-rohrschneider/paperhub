import { initializeApp } from "firebase/app";
import { getAuth, signInWithEmailAndPassword } from "firebase/auth";
import firebaseConfig from "./firebase-config.json" with { type: "json" };

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

const login = async (email: string, password: string) => {
  try {
    const userCredential = await signInWithEmailAndPassword(
      auth,
      email,
      password,
    );
    const user = userCredential.user;
    console.log("Logged in as:", user.email);
    console.log("\nToken:\n\n", await user.getIdToken());
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

login(email, password);
