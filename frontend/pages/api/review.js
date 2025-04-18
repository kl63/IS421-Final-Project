// Next.js API route that proxies requests to the backend
import axios from 'axios';

// Get the backend URL from environment variable or use default
const BACKEND_URL = process.env.BACKEND_URL || process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ message: 'Method not allowed' });
  }

  console.log('API route handler: Proxying to backend:', BACKEND_URL);

  try {
    // Forward the request to the backend with longer timeout
    const response = await axios.post(`${BACKEND_URL}/review`, req.body, {
      timeout: 90000, // 90 second timeout
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    // Return the response from the backend
    return res.status(response.status).json(response.data);
  } catch (error) {
    console.error('Error proxying to backend:', error.message);
    
    // Provide details about the error for debugging
    const errorDetails = {
      message: 'Error connecting to backend service',
      details: error.message,
      backendUrl: BACKEND_URL
    };
    
    // Handle different types of errors
    if (error.response) {
      // The backend responded with a status code outside the 2xx range
      return res.status(error.response.status).json({
        ...errorDetails,
        backendError: error.response.data
      });
    } else if (error.request) {
      // The request was made but no response was received (timeout, etc)
      return res.status(503).json({
        ...errorDetails,
        error: 'Backend service unavailable or timed out. If this is the first request, try again as the backend may need time to wake up.'
      });
    } else {
      // Something else went wrong
      return res.status(500).json({
        ...errorDetails,
        error: 'An unexpected error occurred'
      });
    }
  }
}
