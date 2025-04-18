import React from 'react';

const LoadingState = () => {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <div className="w-16 h-16 border-4 border-primary-200 border-t-primary-600 rounded-full animate-spin mb-4"></div>
      <h2 className="text-xl font-semibold text-gray-700 mb-1">Analyzing Code</h2>
      <p className="text-gray-500">This may take a moment depending on repository size</p>
    </div>
  );
};

export default LoadingState;
