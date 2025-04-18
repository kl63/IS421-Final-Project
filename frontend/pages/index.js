import React, { useState } from 'react';
import Head from 'next/head';
import Header from '../components/Header';
import ReviewForm from '../components/ReviewForm';
import ReviewResults from '../components/ReviewResults';
import LoadingSpinner from '../components/LoadingSpinner';
import { FaMoon, FaSun } from 'react-icons/fa';

export default function Home() {
  const [loading, setLoading] = useState(false);
  const [darkMode, setDarkMode] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleReviewSubmit = async (formData) => {
    try {
      setLoading(true);
      setError(null);
      setResults(null);
      
      // Make API request to backend for code review
      const response = await fetch('/api/review', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Failed to perform code review');
      }
      
      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError(err.message || 'An unexpected error occurred');
      console.error('Error during code review:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleExportMarkdown = () => {
    if (!results) return;
    
    let markdown = `# Code Review Results\n\n`;
    
    // Add summary
    if (results.summary) {
      markdown += `## Summary\n\n${results.summary}\n\n`;
    }
    
    // Add issues
    markdown += `## Issues Found (${results.issues.length})\n\n`;
    results.issues.forEach((issue, index) => {
      markdown += `### ${index + 1}. ${issue.title}\n\n`;
      markdown += `**File:** \`${issue.file_path}\`\n\n`;
      if (issue.line_numbers && issue.line_numbers.length > 0) {
        markdown += `**Line(s):** ${issue.line_numbers.join(', ')}\n\n`;
      }
      markdown += `**Labels:** ${issue.labels.join(', ')}\n\n`;
      markdown += `${issue.description}\n\n`;
      
      if (issue.suggestion) {
        markdown += `**Suggestion:** ${issue.suggestion}\n\n`;
      }
      
      if (issue.code_example) {
        markdown += `\`\`\`javascript\n${issue.code_example}\n\`\`\`\n\n`;
      }
    });
    
    // Add test suggestions
    if (results.test_suggestions && results.test_suggestions.length > 0) {
      markdown += `## Test Suggestions (${results.test_suggestions.length})\n\n`;
      results.test_suggestions.forEach((test, index) => {
        markdown += `### Test ${index + 1}: ${test.file_path}\n\n`;
        markdown += `${test.test_description}\n\n`;
        
        if (test.test_case_example) {
          markdown += `\`\`\`javascript\n${test.test_case_example}\n\`\`\`\n\n`;
        }
      });
    }
    
    // Create a blob and download
    const blob = new Blob([markdown], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'code_review_results.md';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
    document.documentElement.classList.toggle('dark');
  };

  return (
    <div className={`min-h-screen ${darkMode ? 'dark' : ''}`}>
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200">
        <Head>
          <title>Code Review Assistant</title>
          <meta name="description" content="AI-powered code review assistant" />
          <link rel="icon" href="/favicon.ico" />
        </Head>

        <Header />

        <main className="container mx-auto px-4 py-6 sm:px-6 md:py-8">
          <div className="flex justify-end mb-4">
            <button
              onClick={toggleDarkMode}
              className="p-2 rounded-lg bg-white dark:bg-gray-800 shadow-sm border border-gray-200 dark:border-gray-700 text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
              aria-label={darkMode ? 'Switch to light mode' : 'Switch to dark mode'}
            >
              {darkMode ? <FaSun className="text-yellow-400" /> : <FaMoon className="text-gray-600" />}
            </button>
          </div>

          {!results && !loading && (
            <div className="max-w-3xl mx-auto">
              <ReviewForm onSubmit={handleReviewSubmit} />
            </div>
          )}

          {loading && (
            <div className="max-w-3xl mx-auto bg-white dark:bg-gray-800 rounded-xl shadow-soft p-6 mt-4">
              <LoadingSpinner text="Analyzing code... This may take a few moments" />
            </div>
          )}

          {error && (
            <div className="max-w-3xl mx-auto bg-white dark:bg-gray-800 rounded-xl shadow-soft mt-4 overflow-hidden">
              <div className="bg-red-50 dark:bg-red-900/20 border-b border-red-100 dark:border-red-900/30 p-4">
                <h3 className="text-lg font-medium text-red-800 dark:text-red-400">Error</h3>
              </div>
              <div className="p-6">
                <p className="text-red-600 dark:text-red-400">{error}</p>
                <button
                  onClick={() => {
                    setError(null);
                    setResults(null);
                  }}
                  className="mt-4 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-lg shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                >
                  Try Again
                </button>
              </div>
            </div>
          )}

          {results && !loading && !error && (
            <div className="animate-fadeIn">
              <ReviewResults 
                results={results} 
                onExportMarkdown={handleExportMarkdown}
                onReviewAgain={() => setResults(null)} 
              />
            </div>
          )}
        </main>

        <footer className="bg-white dark:bg-gray-800 border-t border-gray-100 dark:border-gray-700 py-6 mt-10">
          <div className="container mx-auto px-4 text-center">
            <p className="text-sm text-gray-500 dark:text-gray-400">
              &copy; {new Date().getFullYear()} Code Review Assistant | 
              Powered by AI
            </p>
          </div>
        </footer>
      </div>
    </div>
  );
}
