// Environment configuration for API endpoint
// Use REACT_APP_API_URL from environment variables or fallback to localhost for development

export const config = {
    apiUrl: process.env.REACT_APP_API_URL || 'http://localhost:5000',
    
    // Speech synthesis configuration
    speech: {
        preferredVoice: 'Microsoft Libby Online (Natural) - English (United Kingdom)',
        pitch: 1.8,
        rate: 1.1,
    },
    
    // Input validation
    maxInputLength: 1000,
    maxFeedbackLength: 2000,
};
