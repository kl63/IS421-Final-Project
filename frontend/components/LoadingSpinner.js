import React from 'react';

const LoadingSpinner = ({ text = 'Loading...' }) => {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <div className="w-12 h-12 rounded-full border-4 border-gray-200">
        <div className="w-full h-full rounded-full border-4 border-t-primary-600 animate-spin"></div>
      </div>
      <p className="mt-4 text-gray-600 text-sm font-medium">{text}</p>
    </div>
  );
};

export default LoadingSpinner;
