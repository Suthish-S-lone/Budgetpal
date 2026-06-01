/**
 * Firebase Configuration
 * 
 * IMPORTANT: This file should NOT be committed to version control
 * in production. For development/college projects, it's acceptable
 * to have this file, but make sure to:
 * 1. Add it to .gitignore
 * 2. Create a config.example.js template
 * 3. Use Firebase security rules to protect your database
 */

const CONFIG = {
    // Firebase Configuration
    firebase: {
        apiKey: "AIzaSyDwEfpM5cLiv95U6GICX0aJj2MjV8mWqfs",
        authDomain: "budgetpal-470505.firebaseapp.com",
        projectId: "budgetpal-470505",
        storageBucket: "budgetpal-470505.firebasestorage.app",
        messagingSenderId: "513174377104",
        appId: "1:513174377104:web:7844bfb5646bfb470fbe15",
        measurementId: "G-ZE9GR76DBB"
    },
    
    // API Configuration
    api: {
        baseUrl: 'http://127.0.0.1:5000',
        // For production, you would change this to your deployed backend URL
        // baseUrl: 'https://your-backend-url.com'
    },
    
    // App Configuration
    app: {
        name: 'BudgetPal',
        version: '1.0.0',
        environment: 'development' // or 'production'
    }
};

// Freeze the config to prevent accidental modifications
Object.freeze(CONFIG);
Object.freeze(CONFIG.firebase);
Object.freeze(CONFIG.api);
Object.freeze(CONFIG.app);