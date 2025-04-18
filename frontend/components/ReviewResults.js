import React, { useState } from 'react';
import { FaClipboard, FaDownload, FaRedo, FaExclamationTriangle, FaCheckCircle, FaInfoCircle, FaCode, FaVial } from 'react-icons/fa';
import ReactMarkdown from 'react-markdown';
import SyntaxHighlighter from 'react-syntax-highlighter';
import { atomOneDark } from 'react-syntax-highlighter/dist/cjs/styles/hljs';

const IssueLabel = ({ label }) => {
  const labelColors = {
    security: 'bg-red-100 text-red-800 border border-red-200',
    style: 'bg-blue-100 text-blue-800 border border-blue-200',
    refactor: 'bg-purple-100 text-purple-800 border border-purple-200',
    test_coverage: 'bg-yellow-100 text-yellow-800 border border-yellow-200',
    performance: 'bg-pink-100 text-pink-800 border border-pink-200',
    documentation: 'bg-green-100 text-green-800 border border-green-200',
    bug: 'bg-orange-100 text-orange-800 border border-orange-200',
  };

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${labelColors[label] || 'bg-gray-100 text-gray-800 border border-gray-200'}`}>
      {label}
    </span>
  );
};

const Tab = ({ label, isActive, count, icon, onClick }) => (
  <button
    className={`px-4 py-3 font-medium text-sm rounded-t-lg flex items-center space-x-2 transition-all ${
      isActive
        ? 'bg-white border-l border-r border-t border-gray-200 text-primary-600 shadow-sm'
        : 'bg-gray-50 text-gray-600 hover:text-gray-800 hover:bg-gray-100'
    }`}
    onClick={onClick}
  >
    {icon}
    <span>{label}</span>
    {count > 0 && (
      <span className={`ml-1.5 px-2 py-0.5 rounded-full text-xs ${isActive ? 'bg-primary-100 text-primary-800' : 'bg-gray-200 text-gray-700'}`}>
        {count}
      </span>
    )}
  </button>
);

const ReviewResults = ({ results, onExportMarkdown, onReviewAgain }) => {
  const [activeTab, setActiveTab] = useState('issues');
  
  const issueCount = results.issues.length;
  const testSuggestionCount = results.test_suggestions.length;
  
  const handleCopyToClipboard = (text) => {
    navigator.clipboard.writeText(text)
      .then(() => {
        alert('Copied to clipboard!');
      })
      .catch((err) => {
        console.error('Could not copy text: ', err);
      });
  };

  const getSeverityIcon = (issue) => {
    // Determine severity based on labels
    if (issue.labels.includes('security') || issue.labels.includes('bug')) {
      return <FaExclamationTriangle className="text-red-500" />;
    } else if (issue.labels.includes('performance') || issue.labels.includes('refactor')) {
      return <FaInfoCircle className="text-yellow-500" />;
    } else {
      return <FaInfoCircle className="text-blue-500" />;
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-soft overflow-hidden transition-all">
      <div className="p-6 border-b border-gray-200">
        <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-4 mb-6">
          <h2 className="text-2xl font-bold text-gray-800">Code Review Results</h2>
          <div className="flex flex-wrap gap-2">
            <button
              onClick={onExportMarkdown}
              className="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-colors"
            >
              <FaDownload className="mr-2 text-gray-500" />
              Export to Markdown
            </button>
            <button
              onClick={onReviewAgain}
              className="inline-flex items-center px-4 py-2 border border-primary-300 shadow-sm text-sm font-medium rounded-lg text-primary-700 bg-primary-50 hover:bg-primary-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-colors"
            >
              <FaRedo className="mr-2 text-primary-500" />
              Review Another
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <div className="bg-white rounded-xl p-4 border border-gray-100 shadow-sm hover:shadow-md transition-shadow">
            <div className="flex items-start">
              <div className="bg-primary-100 p-3 rounded-lg mr-3">
                <FaCode className="text-primary-500" />
              </div>
              <div>
                <div className="text-xs text-gray-500 mb-1">Files Analyzed</div>
                <div className="text-xl font-bold">{results.total_files_analyzed}</div>
              </div>
            </div>
          </div>
          
          <div className="bg-white rounded-xl p-4 border border-gray-100 shadow-sm hover:shadow-md transition-shadow">
            <div className="flex items-start">
              <div className="bg-red-100 p-3 rounded-lg mr-3">
                <FaExclamationTriangle className="text-red-500" />
              </div>
              <div>
                <div className="text-xs text-gray-500 mb-1">Issues Found</div>
                <div className="text-xl font-bold">{issueCount}</div>
              </div>
            </div>
          </div>
          
          <div className="bg-white rounded-xl p-4 border border-gray-100 shadow-sm hover:shadow-md transition-shadow">
            <div className="flex items-start">
              <div className="bg-yellow-100 p-3 rounded-lg mr-3">
                <FaVial className="text-yellow-500" />
              </div>
              <div>
                <div className="text-xs text-gray-500 mb-1">Test Suggestions</div>
                <div className="text-xl font-bold">{testSuggestionCount}</div>
              </div>
            </div>
          </div>
          
          <div className="bg-white rounded-xl p-4 border border-gray-100 shadow-sm hover:shadow-md transition-shadow">
            <div className="flex items-start">
              <div className="bg-gray-100 p-3 rounded-lg mr-3">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-500" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
                </svg>
              </div>
              <div>
                <div className="text-xs text-gray-500 mb-1">Analysis Time</div>
                <div className="text-xl font-bold">{results.analysis_time_seconds.toFixed(2)}s</div>
              </div>
            </div>
          </div>
        </div>

        {results.summary && (
          <div className="mb-6 animate-fadeIn">
            <h3 className="text-lg font-medium text-gray-800 mb-3">Executive Summary</h3>
            <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border-l-4 border-primary-400 p-4 rounded-r-lg">
              <p className="text-gray-800">{results.summary}</p>
            </div>
          </div>
        )}

        <div className="border-b border-gray-200 mb-6">
          <div className="flex space-x-2">
            <Tab 
              label="Issues" 
              count={issueCount}
              icon={<FaExclamationTriangle className={activeTab === 'issues' ? 'text-primary-500' : 'text-gray-400'} />}
              isActive={activeTab === 'issues'} 
              onClick={() => setActiveTab('issues')} 
            />
            <Tab 
              label="Test Suggestions" 
              count={testSuggestionCount}
              icon={<FaVial className={activeTab === 'test-suggestions' ? 'text-primary-500' : 'text-gray-400'} />}
              isActive={activeTab === 'test-suggestions'} 
              onClick={() => setActiveTab('test-suggestions')} 
            />
          </div>
        </div>

        {activeTab === 'issues' && (
          <div className="space-y-6">
            {results.issues.length > 0 ? (
              results.issues.map((issue, index) => (
                <div key={index} className="border border-gray-200 rounded-xl overflow-hidden transition-all hover:shadow-md">
                  <div className="flex items-center bg-gray-50 px-4 py-3 border-b border-gray-200">
                    <div className="mr-2">{getSeverityIcon(issue)}</div>
                    <div className="mr-auto font-medium">{issue.title}</div>
                    <div className="flex flex-wrap gap-1 ml-2">
                      {issue.labels.map((label, i) => (
                        <IssueLabel key={i} label={label} />
                      ))}
                    </div>
                  </div>
                  <div className="p-4 bg-white">
                    <div className="mb-3">
                      <span className="text-sm font-medium text-gray-500">File: </span>
                      <code className="text-sm bg-gray-100 px-1.5 py-0.5 rounded">{issue.file_path}</code>
                      {issue.line_numbers && issue.line_numbers.length > 0 && (
                        <span className="text-sm ml-2">
                          Line(s): {issue.line_numbers.join(', ')}
                        </span>
                      )}
                    </div>
                    <p className="text-gray-700 mb-4">{issue.description}</p>
                    
                    {issue.suggestion && (
                      <div className="mb-4 bg-green-50 border-l-4 border-green-400 p-3 rounded-r-lg">
                        <h4 className="text-sm font-medium text-gray-700 mb-1">Suggestion:</h4>
                        <p className="text-gray-800">{issue.suggestion}</p>
                      </div>
                    )}
                    
                    {issue.code_example && (
                      <div>
                        <div className="flex justify-between items-center mb-2">
                          <h4 className="text-sm font-medium text-gray-700">Example Code:</h4>
                          <button
                            onClick={() => handleCopyToClipboard(issue.code_example)}
                            className="text-xs text-gray-500 hover:text-gray-700 flex items-center bg-gray-100 hover:bg-gray-200 px-2 py-1 rounded transition-colors"
                          >
                            <FaClipboard className="mr-1" /> Copy
                          </button>
                        </div>
                        <SyntaxHighlighter 
                          language="javascript" 
                          style={atomOneDark}
                          customStyle={{ borderRadius: '0.5rem' }}
                          wrapLines={true}
                        >
                          {issue.code_example}
                        </SyntaxHighlighter>
                      </div>
                    )}
                  </div>
                </div>
              ))
            ) : (
              <div className="text-center py-16 bg-green-50 rounded-xl border border-green-100">
                <FaCheckCircle className="mx-auto text-green-500 text-4xl mb-3" />
                <h3 className="text-lg font-medium text-gray-800 mb-1">All Clear!</h3>
                <p className="text-gray-600">No issues found in the code review.</p>
              </div>
            )}
          </div>
        )}

        {activeTab === 'test-suggestions' && (
          <div className="space-y-6">
            {results.test_suggestions.length > 0 ? (
              results.test_suggestions.map((test, index) => (
                <div key={index} className="border border-gray-200 rounded-xl overflow-hidden transition-all hover:shadow-md">
                  <div className="bg-yellow-50 px-4 py-3 border-b border-gray-200 font-medium flex items-center">
                    <FaVial className="text-yellow-500 mr-2" />
                    Test for <code className="text-sm bg-yellow-100 ml-2 px-2 py-0.5 rounded">{test.file_path}</code>
                  </div>
                  <div className="p-4 bg-white">
                    <p className="text-gray-700 mb-4">{test.test_description}</p>
                    
                    {test.test_case_example && (
                      <div>
                        <div className="flex justify-between items-center mb-2">
                          <h4 className="text-sm font-medium text-gray-700">Example Test:</h4>
                          <button
                            onClick={() => handleCopyToClipboard(test.test_case_example)}
                            className="text-xs text-gray-500 hover:text-gray-700 flex items-center bg-gray-100 hover:bg-gray-200 px-2 py-1 rounded transition-colors"
                          >
                            <FaClipboard className="mr-1" /> Copy
                          </button>
                        </div>
                        <SyntaxHighlighter 
                          language="javascript" 
                          style={atomOneDark}
                          customStyle={{ borderRadius: '0.5rem' }}
                          wrapLines={true}
                        >
                          {test.test_case_example}
                        </SyntaxHighlighter>
                      </div>
                    )}
                  </div>
                </div>
              ))
            ) : (
              <div className="text-center py-16 bg-gray-50 rounded-xl border border-gray-200">
                <FaVial className="mx-auto text-gray-400 text-4xl mb-3" />
                <h3 className="text-lg font-medium text-gray-800 mb-1">No Test Suggestions</h3>
                <p className="text-gray-600">No test suggestions are available for this code review.</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default ReviewResults;
