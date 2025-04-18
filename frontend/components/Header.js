import React from 'react';
import { FaGithub, FaCode, FaSearch } from 'react-icons/fa';

const Header = () => {
  return (
    <header className="bg-white border-b border-gray-100 sticky top-0 z-10 shadow-sm">
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        <div className="flex items-center space-x-3">
          <div className="bg-primary-600 text-white p-2 rounded-lg">
            <FaCode className="text-xl" />
          </div>
          <div>
            <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary-600 to-primary-800">
              Code Review Assistant
            </h1>
            <p className="text-xs text-gray-500 hidden sm:block">AI-powered code analysis</p>
          </div>
        </div>
        
        <div className="flex items-center gap-3">
          <a
            href="/docs" 
            className="text-sm text-gray-600 hover:text-primary-600 transition-colors hidden md:flex items-center space-x-1"
          >
            <FaSearch className="text-sm" />
            <span>API Docs</span>
          </a>
          
          <a 
            href="https://github.com/kl63/Crispy-Crown-BE" 
            target="_blank" 
            rel="noopener noreferrer"
            className="flex items-center space-x-2 text-gray-600 hover:text-primary-600 transition-colors bg-gray-50 hover:bg-gray-100 px-3 py-1.5 rounded-full text-sm"
          >
            <FaGithub className="text-lg" />
            <span className="hidden md:block">View on GitHub</span>
          </a>
        </div>
      </div>
    </header>
  );
};

export default Header;
