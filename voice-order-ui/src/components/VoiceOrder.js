import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { signOut } from "firebase/auth";
import { auth } from '../firebase';
import axios from 'axios';
import innsightLogo from '../components/innsight_logo_png.png';
import { config } from '../config';

// IMPORTS BY CHRIS
import 'bootstrap/dist/css/bootstrap.min.css';
import './VoiceOrder.css';
import Form from 'react-bootstrap/Form';

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

const getSpeechErrorMessage = (errorCode) => {
    switch (errorCode) {
        case 'network':
            return 'Speech recognition network error. Ensure you are online, using HTTPS (or localhost), and try again.';
        case 'not-allowed':
        case 'service-not-allowed':
            return 'Microphone access was denied. Please allow microphone permission in your browser settings.';
        case 'no-speech':
            return 'No speech detected. Please speak clearly and try again.';
        case 'audio-capture':
            return 'No microphone was found. Check your microphone connection and browser permissions.';
        case 'aborted':
            return 'Speech recognition was cancelled. Please try again.';
        default:
            return `Voice recognition error: ${errorCode}. Please try again.`;
    }
};

const VoiceOrder = () => {
    const [input, setInput] = useState('');
    const [response, setResponse] = useState('');
    const [loading, setLoading] = useState(false);
    const [feedback, setFeedback] = useState('');
    const [chosenVoice, setChosenVoice] = useState(null);
    const [error, setError] = useState('');
    const navigate = useNavigate();

    // Memoize API URL to avoid recreating on every render
    const apiUrl = useMemo(() => config.apiUrl, []);

    // Load preferred voice for text-to-speech (optimized with useCallback)
    const loadVoices = useCallback(() => {
        const voices = speechSynthesis.getVoices();
        if (voices.length === 0) return; // Wait for voices to load
        
        const selectedVoice = voices.find(voice => voice.name === config.speech.preferredVoice);
        
        if (selectedVoice) {
            console.log("Selected voice:", selectedVoice);
            setChosenVoice(selectedVoice);
        } else {
            console.warn("Preferred voice not found, using default voice.");
            setChosenVoice(voices[0]);
        }
    }, []);

    useEffect(() => {
        loadVoices();
        // Some browsers need to wait for voiceschanged event
        if (speechSynthesis.onvoiceschanged !== undefined) {
            speechSynthesis.onvoiceschanged = loadVoices;
        }
        
        return () => {
            speechSynthesis.onvoiceschanged = null;
        };
    }, [loadVoices]);

    // Start voice recognition (optimized with useCallback)
    const startVoiceRecognition = useCallback(async () => {
        if (!SpeechRecognition) {
            setError("Your browser does not support Speech Recognition.");
            return;
        }

        if (!window.isSecureContext && window.location.hostname !== 'localhost') {
            setError('Voice recognition requires HTTPS. Please open the deployed HTTPS URL and try again.');
            return;
        }

        if (!navigator.onLine) {
            setError('You appear to be offline. Speech recognition requires an internet connection.');
            return;
        }

        // Ask browser for microphone permission first to avoid opaque recognition failures.
        try {
            await navigator.mediaDevices.getUserMedia({ audio: true });
        } catch (permissionError) {
            setError('Microphone permission is required. Please allow microphone access and try again.');
            return;
        }

        const recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';

        recognition.onstart = () => {
            console.log('Voice recognition started. Speak into the microphone.');
            setError(''); // Clear any previous errors
        };

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            setInput(transcript);
            console.log('You said: ', transcript);
        };

        recognition.onerror = (event) => {
            console.error('Speech recognition error: ', event.error);
            setError(getSpeechErrorMessage(event.error));
        };

        recognition.onend = () => {
            console.log('Voice recognition ended.');
        };

        recognition.start();
    }, []);

    // Speak response using text-to-speech (optimized with useCallback)
    const speakResponse = useCallback((responseText) => {
        if (!chosenVoice) return;
        
        const utterance = new SpeechSynthesisUtterance(responseText);
        utterance.voice = chosenVoice;
        utterance.pitch = config.speech.pitch;
        utterance.rate = config.speech.rate;

        window.speechSynthesis.speak(utterance);
    }, [chosenVoice]);

    // Handle the voice order submission (optimized with useCallback)
    const handleVoiceOrder = useCallback(async () => {
        const trimmedInput = input.trim();
        
        if (!trimmedInput) {
            setError('Please provide a voice input or type a request before submitting.');
            return;
        }

        if (trimmedInput.length > config.maxInputLength) {
            setError(`Request is too long (max ${config.maxInputLength} characters).`);
            return;
        }

        setLoading(true);
        setError('');
        
        try {
            // Send order to the backend API
            const res = await axios.post(`${apiUrl}/api/voice-order`, { input: trimmedInput }, {
                timeout: 10000, // 10 second timeout
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            // Check response from server and update response state
            if (res.data && res.data.response) {
                setResponse(res.data.response);
                speakResponse(res.data.response);
            } else {
                setResponse('Unexpected response format from the server.');
            }

            setInput(''); // Clear input field
        } catch (error) {
            let errorMessage = 'An error occurred. Please try again.';
            
            if (error.response) {
                // Server responded with error
                errorMessage = error.response.data?.error || error.response.statusText;
            } else if (error.request) {
                // Request made but no response
                errorMessage = 'No response from the server. Please check your network connection.';
            } else if (error.code === 'ECONNABORTED') {
                errorMessage = 'Request timed out. Please try again.';
            } else {
                errorMessage = error.message;
            }
            
            setError(errorMessage);
            setResponse('');
        } finally {
            setLoading(false);
        }
    }, [input, apiUrl, speakResponse]);

    // Handle feedback submission to backend API (optimized with useCallback)
    const handleFeedback = useCallback(async () => {
        const trimmedFeedback = feedback.trim();
        
        if (!trimmedFeedback) {
            setError('Please provide your feedback.');
            return;
        }

        if (trimmedFeedback.length > config.maxFeedbackLength) {
            setError(`Feedback is too long (max ${config.maxFeedbackLength} characters).`);
            return;
        }

        try {
            await axios.post(`${apiUrl}/api/feedback`, { feedback: trimmedFeedback }, {
                timeout: 5000,
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            setFeedback('');
            setError('');
            alert('Thank you for your feedback!');
        } catch (error) {
            console.error('Feedback submission error:', error);
            setError('Error submitting feedback. Please try again.');
        }
    }, [feedback, apiUrl]);

    // Handle user logout and redirect to login page (optimized with useCallback)
    const handleLogout = useCallback(async () => {
        try {
            await signOut(auth);
            navigate("/login");
        } catch (error) {
            console.error('Logout failed:', error);
            setError('Logout failed. Please try again.');
        }
    }, [navigate]);

    return (
        <div className="order-page">
            <div className="order-container"> 
            <img src={innsightLogo} alt="logo" />
            <p><b>INNSIGHT</b></p>
                
                {/* Error display */}
                {error && (
                    <div className="alert alert-danger" role="alert">
                        {error}
                    </div>
                )}
                
                <div>
                    <Form.Group className="mb-3" controlId="requestArea">
                        <Form.Label><b>Request:</b></Form.Label>
                        <Form.Control
                            as="textarea"
                            value={input}
                            onChange={(e) => {
                                setInput(e.target.value);
                                setError(''); // Clear error when user types
                            }}
                            rows={4}
                            placeholder="Type your request here..."
                            maxLength={config.maxInputLength}
                            disabled={loading}
                        />
                        <Form.Text className="text-muted">
                            {input.length}/{config.maxInputLength} characters
                        </Form.Text>
                    </Form.Group>
                    <button 
                        onClick={startVoiceRecognition} 
                        disabled={loading}
                        className="btn btn-primary me-2"
                    >
                        🎤 Start Voice Input
                    </button>
                    <button 
                        onClick={handleVoiceOrder} 
                        disabled={loading || !input.trim()}
                        className="btn btn-success"
                    >
                        {loading ? 'Processing...' : '📤 Submit Order'}
                    </button>
                </div>
                
                {response && (
                    <div className="response-container alert alert-success mt-3">
                        <p><b>Response:</b></p>
                        <p>{response}</p>
                    </div>
                )}
                
                <div className="mt-4">
                    <Form.Group className="mb-3" controlId="feedbackArea">
                        <Form.Label><b>Feedback:</b></Form.Label>
                        <Form.Control
                            as="textarea"
                            value={feedback}
                            onChange={(e) => {
                                setFeedback(e.target.value);
                                setError('');
                            }}
                            rows={2}
                            placeholder="Provide feedback here..."
                            maxLength={config.maxFeedbackLength}
                        />
                        <Form.Text className="text-muted">
                            {feedback.length}/{config.maxFeedbackLength} characters
                        </Form.Text>
                    </Form.Group>
                    <button 
                        onClick={handleFeedback}
                        className="btn btn-info me-2"
                        disabled={!feedback.trim()}
                    >
                        💬 Submit Feedback
                    </button>
                    <button 
                        onClick={handleLogout}
                        className="btn btn-secondary"
                    >
                        🚪 Logout
                    </button>
                </div>
            </div>
        </div>
    );
};

export default VoiceOrder;
