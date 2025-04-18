import React, { useState } from 'react';
import { FaGithub, FaCodeBranch, FaCog, FaArrowRight, FaChevronDown, FaChevronUp } from 'react-icons/fa';

const ReviewForm = ({ onSubmit }) => {
  const [url, setUrl] = useState('');
  const [filePaths, setFilePaths] = useState('');
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [settings, setSettings] = useState({
    tone: 'neutral',
    apply_labels: false,
    include_test_suggestions: true,
    include_summary: true,
    max_issues: 10
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Prepare form data
    const formData = {
      url,
      file_paths: filePaths ? filePaths.split('\n').map(path => path.trim()).filter(Boolean) : null,
      settings
    };
    
    onSubmit(formData);
  };

  const handleSettingsChange = (e) => {
    const { name, value, type, checked } = e.target;
    setSettings({
      ...settings,
      [name]: type === 'checkbox' ? checked : value
    });
  };

  return (
    <div className="bg-white rounded-xl shadow-soft overflow-hidden">
      <div className="border-b border-gray-100 bg-gradient-to-r from-primary-50 to-white px-6 py-4">
        <h2 className="text-lg font-semibold text-gray-800">Submit Repository for Review</h2>
        <p className="text-sm text-gray-600">Enter a GitHub repository or pull request URL to begin analysis</p>
      </div>

      <form onSubmit={handleSubmit} className="p-6 space-y-6">
        {/* GitHub URL input */}
        <div className="space-y-2">
          <label 
            htmlFor="github-url" 
            className="block text-sm font-medium text-gray-700"
          >
            GitHub Repository or Pull Request URL
          </label>
          <div className="relative group">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-400 group-focus-within:text-primary-500">
              <FaGithub className="text-lg" />
            </div>
            <input
              id="github-url"
              type="url"
              placeholder="https://github.com/username/repo or PR URL"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              className="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 
                focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all"
              required
            />
          </div>
          <p className="mt-1 text-xs text-gray-500">
            Enter the full URL to a GitHub repository or pull request
          </p>
        </div>

        {/* Specific file paths */}
        <div className="space-y-2">
          <label 
            htmlFor="file-paths" 
            className="block text-sm font-medium text-gray-700"
          >
            Specific File Paths (Optional)
          </label>
          <div className="relative group">
            <div className="absolute inset-y-0 left-0 pl-3 pt-3 pointer-events-none text-gray-400 group-focus-within:text-primary-500">
              <FaCodeBranch className="text-lg" />
            </div>
            <textarea
              id="file-paths"
              placeholder="src/main.js&#10;app/models.py&#10;lib/utils.js"
              value={filePaths}
              onChange={(e) => setFilePaths(e.target.value)}
              className="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 
                focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all h-24"
            />
          </div>
          <p className="mt-1 text-xs text-gray-500">
            Enter file paths to review (one per line) or leave empty to scan the entire repository
          </p>
        </div>

        {/* Advanced Settings Toggle */}
        <div>
          <button
            type="button"
            className="flex items-center text-sm text-primary-600 hover:text-primary-700 font-medium focus:outline-none transition-colors"
            onClick={() => setShowAdvanced(!showAdvanced)}
          >
            <FaCog className="mr-2" />
            {showAdvanced ? 'Hide Advanced Settings' : 'Show Advanced Settings'}
            {showAdvanced ? <FaChevronUp className="ml-1" /> : <FaChevronDown className="ml-1" />}
          </button>
        </div>

        {/* Advanced Settings */}
        {showAdvanced && (
          <div className="p-4 bg-gray-50 rounded-xl space-y-5 border border-gray-100">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Review Tone
              </label>
              <select
                name="tone"
                value={settings.tone}
                onChange={handleSettingsChange}
                className="block w-full border border-gray-300 rounded-lg shadow-sm p-2.5 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all"
              >
                <option value="strict">Strict - Focus on identifying all issues</option>
                <option value="mentor">Mentor - Educational and constructive</option>
                <option value="neutral">Neutral - Balanced feedback</option>
              </select>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-3">
                <label className="flex items-center text-sm">
                  <input
                    type="checkbox"
                    name="apply_labels"
                    checked={settings.apply_labels}
                    onChange={handleSettingsChange}
                    className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  />
                  <span className="ml-2 text-gray-700">
                    Apply labels to PR
                  </span>
                </label>

                <label className="flex items-center text-sm">
                  <input
                    type="checkbox"
                    name="include_test_suggestions"
                    checked={settings.include_test_suggestions}
                    onChange={handleSettingsChange}
                    className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  />
                  <span className="ml-2 text-gray-700">
                    Include test suggestions
                  </span>
                </label>

                <label className="flex items-center text-sm">
                  <input
                    type="checkbox"
                    name="include_summary"
                    checked={settings.include_summary}
                    onChange={handleSettingsChange}
                    className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  />
                  <span className="ml-2 text-gray-700">
                    Include summary
                  </span>
                </label>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Maximum Issues to Report
                </label>
                <input
                  type="number"
                  name="max_issues"
                  min="1"
                  max="50"
                  value={settings.max_issues}
                  onChange={handleSettingsChange}
                  className="block w-full border border-gray-300 rounded-lg shadow-sm p-2.5 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all"
                />
              </div>
            </div>
          </div>
        )}

        {/* Submit Button */}
        <div>
          <button
            type="submit"
            className="w-full flex items-center justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-colors"
          >
            <span>Analyze Code</span>
            <FaArrowRight className="ml-2" />
          </button>
        </div>
      </form>
    </div>
  );
};

export default ReviewForm;
