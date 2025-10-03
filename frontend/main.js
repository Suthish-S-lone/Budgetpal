// Firebase Configuration
import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider, signInWithPopup, signOut, onAuthStateChanged } from "firebase/auth";
import { getAnalytics } from "firebase/analytics";

// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyDwEfpM5cLiv95U6GICX0aJj2MjV8mWqfs",
    authDomain: "budgetpal-470505.firebaseapp.com",
    projectId: "budgetpal-470505",
    storageBucket: "budgetpal-470505.firebasestorage.app",
    messagingSenderId: "513174377104",
    appId: "1:513174377104:web:7844bfb5646bfb470fbe15",
    measurementId: "G-ZE9GR76DBB"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

class AuthManager {
    constructor() {
        this.initializeElements();
        this.bindEvents();
        this.initializeAuthObserver();
    }

    initializeElements() {
        this.elements = {
            loginBtn: document.getElementById('login-btn'),
            logoutBtn: document.getElementById('logout-btn'),
            userNameEl: document.getElementById('user-name'),
            loggedInEls: document.querySelectorAll('.logged-in'),
            loggedOutEls: document.querySelectorAll('.logged-out')
        };
    }

    bindEvents() {
        this.elements.loginBtn?.addEventListener('click', () => this.handleLogin());
        this.elements.logoutBtn?.addEventListener('click', () => this.handleLogout());
    }

    async handleLogin() {
        try {
            const result = await signInWithPopup(auth, provider);
            console.log("User signed in:", result.user);
        } catch (error) {
            console.error("Authentication failed:", error);
        }
    }

    async handleLogout() {
        try {
            await signOut(auth);
            console.log("User signed out");
        } catch (error) {
            console.error("Sign out failed:", error);
        }
    }

    initializeAuthObserver() {
        onAuthStateChanged(auth, (user) => {
            if (user) {
                this.handleUserSignedIn(user);
            } else {
                this.handleUserSignedOut();
            }
        });
    }

    handleUserSignedIn(user) {
        console.log("Auth state changed: Logged in as", user.displayName);
        
        if (this.elements.userNameEl) {
            this.elements.userNameEl.textContent = user.displayName;
        }
        
        this.toggleElementsVisibility(true);
    }

    handleUserSignedOut() {
        console.log("Auth state changed: Logged out");
        
        if (this.elements.userNameEl) {
            this.elements.userNameEl.textContent = 'Guest';
        }
        
        this.toggleElementsVisibility(false);
    }

    toggleElementsVisibility(isSignedIn) {
        this.elements.loggedInEls.forEach(el => {
            el.style.display = isSignedIn ? 'block' : 'none';
        });
        
        this.elements.loggedOutEls.forEach(el => {
            el.style.display = isSignedIn ? 'none' : 'block';
        });
    }
}

// Initialize the authentication manager when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new AuthManager();
});