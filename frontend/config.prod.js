/**
 * Production Firebase Configuration
 * 
 * This file is safe to deploy as Firebase config is meant to be public.
 * Security is handled by Firebase Security Rules and backend authentication.
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
    
    // API Configuration - UPDATE THIS WITH YOUR CLOUD RUN URL
    api: {
        baseUrl: 'https://budgetpal-api-513174377104.us-central1.run.app',
        // IMPORTANT: Replace XXXXXX with your actual Cloud Run service URL
    },
    
    // App Configuration
    app: {
        name: 'BudgetPal',
        version: '1.0.0',
        environment: 'production'
    }
};

// Freeze the config to prevent accidental modifications
Object.freeze(CONFIG);
Object.freeze(CONFIG.firebase);
Object.freeze(CONFIG.api);
Object.freeze(CONFIG.app);