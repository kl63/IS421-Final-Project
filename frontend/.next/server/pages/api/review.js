"use strict";
/*
 * ATTENTION: An "eval-source-map" devtool has been used.
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file with attached SourceMaps in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
(() => {
var exports = {};
exports.id = "pages/api/review";
exports.ids = ["pages/api/review"];
exports.modules = {

/***/ "axios":
/*!************************!*\
  !*** external "axios" ***!
  \************************/
/***/ ((module) => {

module.exports = import("axios");;

/***/ }),

/***/ "(api)/./pages/api/review.js":
/*!*****************************!*\
  !*** ./pages/api/review.js ***!
  \*****************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.a(module, async (__webpack_handle_async_dependencies__, __webpack_async_result__) => { try {\n__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   \"default\": () => (/* binding */ handler)\n/* harmony export */ });\n/* harmony import */ var axios__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! axios */ \"axios\");\nvar __webpack_async_dependencies__ = __webpack_handle_async_dependencies__([axios__WEBPACK_IMPORTED_MODULE_0__]);\naxios__WEBPACK_IMPORTED_MODULE_0__ = (__webpack_async_dependencies__.then ? (await __webpack_async_dependencies__)() : __webpack_async_dependencies__)[0];\n// Next.js API route that proxies requests to the backend\n\n// Get the backend URL from environment variable or use default\nconst BACKEND_URL = \"http://localhost:8000\" || 0;\nasync function handler(req, res) {\n    if (req.method !== \"POST\") {\n        return res.status(405).json({\n            message: \"Method not allowed\"\n        });\n    }\n    try {\n        // Forward the request to the backend\n        const response = await axios__WEBPACK_IMPORTED_MODULE_0__[\"default\"].post(`${BACKEND_URL}/review`, req.body);\n        // Return the response from the backend\n        return res.status(response.status).json(response.data);\n    } catch (error) {\n        console.error(\"Error proxying to backend:\", error);\n        // Handle different types of errors\n        if (error.response) {\n            // The backend responded with a status code outside the 2xx range\n            return res.status(error.response.status).json(error.response.data);\n        } else if (error.request) {\n            // The request was made but no response was received\n            return res.status(503).json({\n                message: \"Unable to connect to backend service. Please make sure the backend server is running.\"\n            });\n        } else {\n            // Something else went wrong\n            return res.status(500).json({\n                message: \"An error occurred while processing your request.\"\n            });\n        }\n    }\n}\n\n__webpack_async_result__();\n} catch(e) { __webpack_async_result__(e); } });//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiKGFwaSkvLi9wYWdlcy9hcGkvcmV2aWV3LmpzLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7O0FBQUEseURBQXlEO0FBQy9CO0FBRTFCLCtEQUErRDtBQUMvRCxNQUFNQyxjQUFjQyx1QkFBbUMsSUFBSTtBQUU1QyxlQUFlRyxRQUFRQyxHQUFHLEVBQUVDLEdBQUcsRUFBRTtJQUM5QyxJQUFJRCxJQUFJRSxNQUFNLEtBQUssUUFBUTtRQUN6QixPQUFPRCxJQUFJRSxNQUFNLENBQUMsS0FBS0MsSUFBSSxDQUFDO1lBQUVDLFNBQVM7UUFBcUI7SUFDOUQsQ0FBQztJQUVELElBQUk7UUFDRixxQ0FBcUM7UUFDckMsTUFBTUMsV0FBVyxNQUFNWixrREFBVSxDQUFDLENBQUMsRUFBRUMsWUFBWSxPQUFPLENBQUMsRUFBRUssSUFBSVEsSUFBSTtRQUVuRSx1Q0FBdUM7UUFDdkMsT0FBT1AsSUFBSUUsTUFBTSxDQUFDRyxTQUFTSCxNQUFNLEVBQUVDLElBQUksQ0FBQ0UsU0FBU0csSUFBSTtJQUN2RCxFQUFFLE9BQU9DLE9BQU87UUFDZEMsUUFBUUQsS0FBSyxDQUFDLDhCQUE4QkE7UUFFNUMsbUNBQW1DO1FBQ25DLElBQUlBLE1BQU1KLFFBQVEsRUFBRTtZQUNsQixpRUFBaUU7WUFDakUsT0FBT0wsSUFBSUUsTUFBTSxDQUFDTyxNQUFNSixRQUFRLENBQUNILE1BQU0sRUFBRUMsSUFBSSxDQUFDTSxNQUFNSixRQUFRLENBQUNHLElBQUk7UUFDbkUsT0FBTyxJQUFJQyxNQUFNRSxPQUFPLEVBQUU7WUFDeEIsb0RBQW9EO1lBQ3BELE9BQU9YLElBQUlFLE1BQU0sQ0FBQyxLQUFLQyxJQUFJLENBQUM7Z0JBQzFCQyxTQUFTO1lBQ1g7UUFDRixPQUFPO1lBQ0wsNEJBQTRCO1lBQzVCLE9BQU9KLElBQUlFLE1BQU0sQ0FBQyxLQUFLQyxJQUFJLENBQUM7Z0JBQzFCQyxTQUFTO1lBQ1g7UUFDRixDQUFDO0lBQ0g7QUFDRixDQUFDIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vY29kZS1yZXZpZXctYXNzaXN0YW50LWZyb250ZW5kLy4vcGFnZXMvYXBpL3Jldmlldy5qcz82N2JiIl0sInNvdXJjZXNDb250ZW50IjpbIi8vIE5leHQuanMgQVBJIHJvdXRlIHRoYXQgcHJveGllcyByZXF1ZXN0cyB0byB0aGUgYmFja2VuZFxuaW1wb3J0IGF4aW9zIGZyb20gJ2F4aW9zJztcblxuLy8gR2V0IHRoZSBiYWNrZW5kIFVSTCBmcm9tIGVudmlyb25tZW50IHZhcmlhYmxlIG9yIHVzZSBkZWZhdWx0XG5jb25zdCBCQUNLRU5EX1VSTCA9IHByb2Nlc3MuZW52Lk5FWFRfUFVCTElDX0JBQ0tFTkRfVVJMIHx8ICdodHRwOi8vbG9jYWxob3N0OjgwMDAnO1xuXG5leHBvcnQgZGVmYXVsdCBhc3luYyBmdW5jdGlvbiBoYW5kbGVyKHJlcSwgcmVzKSB7XG4gIGlmIChyZXEubWV0aG9kICE9PSAnUE9TVCcpIHtcbiAgICByZXR1cm4gcmVzLnN0YXR1cyg0MDUpLmpzb24oeyBtZXNzYWdlOiAnTWV0aG9kIG5vdCBhbGxvd2VkJyB9KTtcbiAgfVxuXG4gIHRyeSB7XG4gICAgLy8gRm9yd2FyZCB0aGUgcmVxdWVzdCB0byB0aGUgYmFja2VuZFxuICAgIGNvbnN0IHJlc3BvbnNlID0gYXdhaXQgYXhpb3MucG9zdChgJHtCQUNLRU5EX1VSTH0vcmV2aWV3YCwgcmVxLmJvZHkpO1xuICAgIFxuICAgIC8vIFJldHVybiB0aGUgcmVzcG9uc2UgZnJvbSB0aGUgYmFja2VuZFxuICAgIHJldHVybiByZXMuc3RhdHVzKHJlc3BvbnNlLnN0YXR1cykuanNvbihyZXNwb25zZS5kYXRhKTtcbiAgfSBjYXRjaCAoZXJyb3IpIHtcbiAgICBjb25zb2xlLmVycm9yKCdFcnJvciBwcm94eWluZyB0byBiYWNrZW5kOicsIGVycm9yKTtcbiAgICBcbiAgICAvLyBIYW5kbGUgZGlmZmVyZW50IHR5cGVzIG9mIGVycm9yc1xuICAgIGlmIChlcnJvci5yZXNwb25zZSkge1xuICAgICAgLy8gVGhlIGJhY2tlbmQgcmVzcG9uZGVkIHdpdGggYSBzdGF0dXMgY29kZSBvdXRzaWRlIHRoZSAyeHggcmFuZ2VcbiAgICAgIHJldHVybiByZXMuc3RhdHVzKGVycm9yLnJlc3BvbnNlLnN0YXR1cykuanNvbihlcnJvci5yZXNwb25zZS5kYXRhKTtcbiAgICB9IGVsc2UgaWYgKGVycm9yLnJlcXVlc3QpIHtcbiAgICAgIC8vIFRoZSByZXF1ZXN0IHdhcyBtYWRlIGJ1dCBubyByZXNwb25zZSB3YXMgcmVjZWl2ZWRcbiAgICAgIHJldHVybiByZXMuc3RhdHVzKDUwMykuanNvbih7IFxuICAgICAgICBtZXNzYWdlOiAnVW5hYmxlIHRvIGNvbm5lY3QgdG8gYmFja2VuZCBzZXJ2aWNlLiBQbGVhc2UgbWFrZSBzdXJlIHRoZSBiYWNrZW5kIHNlcnZlciBpcyBydW5uaW5nLicgXG4gICAgICB9KTtcbiAgICB9IGVsc2Uge1xuICAgICAgLy8gU29tZXRoaW5nIGVsc2Ugd2VudCB3cm9uZ1xuICAgICAgcmV0dXJuIHJlcy5zdGF0dXMoNTAwKS5qc29uKHsgXG4gICAgICAgIG1lc3NhZ2U6ICdBbiBlcnJvciBvY2N1cnJlZCB3aGlsZSBwcm9jZXNzaW5nIHlvdXIgcmVxdWVzdC4nIFxuICAgICAgfSk7XG4gICAgfVxuICB9XG59XG4iXSwibmFtZXMiOlsiYXhpb3MiLCJCQUNLRU5EX1VSTCIsInByb2Nlc3MiLCJlbnYiLCJORVhUX1BVQkxJQ19CQUNLRU5EX1VSTCIsImhhbmRsZXIiLCJyZXEiLCJyZXMiLCJtZXRob2QiLCJzdGF0dXMiLCJqc29uIiwibWVzc2FnZSIsInJlc3BvbnNlIiwicG9zdCIsImJvZHkiLCJkYXRhIiwiZXJyb3IiLCJjb25zb2xlIiwicmVxdWVzdCJdLCJzb3VyY2VSb290IjoiIn0=\n//# sourceURL=webpack-internal:///(api)/./pages/api/review.js\n");

/***/ })

};
;

// load runtime
var __webpack_require__ = require("../../webpack-api-runtime.js");
__webpack_require__.C(exports);
var __webpack_exec__ = (moduleId) => (__webpack_require__(__webpack_require__.s = moduleId))
var __webpack_exports__ = (__webpack_exec__("(api)/./pages/api/review.js"));
module.exports = __webpack_exports__;

})();