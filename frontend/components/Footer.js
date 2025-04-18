import React from 'react';

const Footer = () => {
  return (
    <footer className="bg-white border-t border-gray-200 py-6">
      <div className="container mx-auto px-4 text-center text-gray-600">
        <p>© {new Date().getFullYear()} Code Review Assistant | Built with FastAPI and Next.js</p>
      </div>
    </footer>
  );
};

export default Footer;
