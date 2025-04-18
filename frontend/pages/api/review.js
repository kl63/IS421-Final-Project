// Next.js API route that proxies requests to the backend
import axios from 'axios';

// Get the backend URL from environment variable or use default
const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ message: 'Method not allowed' });
  }

  try {
    // Forward the request to the backend
    const response = await axios.post(`${BACKEND_URL}/review`, req.body);
    
    // Return the response from the backend
    return res.status(response.status).json(response.data);
  } catch (error) {
    console.error('Error proxying to backend:', error);
    
    // Handle different types of errors
    if (error.response) {
      // The backend responded with a status code outside the 2xx range
      return res.status(error.response.status).json(error.response.data);
    } else if (error.request) {
      // The request was made but no response was received
      return res.status(503).json({ 
        message: 'Unable to connect to backend service. Please make sure the backend server is running.' 
      });
    } else {
      // Something else went wrong
      return res.status(500).json({ 
        message: 'An error occurred while processing your request.' 
      });
    }
  }
}
