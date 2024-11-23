export const handleErrors = (error, action) => {
  console.error(error.response.data);
  // Check if the error response contains detailed error data

  if (error.response && error.response.data) {
    const errorData = error.response.data;

    if (Array.isArray(errorData.detail)) {
      // Log the first error message if details are provided as an array

      console.error(`Error ${action}:`, errorData.detail[0].msg);
      throw new Error(errorData.detail[0].msg || `Error ${action}`);
    } else {
      // Log the error detail or message if available, otherwise log the general error

      console.error(`Error ${action}:`, error.detail || error.message);
      throw new Error(
        errorData.detail || errorData.message || `Error ${action}`
      );
    }
  } else if (error.message) {
    // Log and throw the error message if available

    console.error(`Error ${action}:`, error.message);
    throw new Error(error.message);
  } else {
    // Fallback error handling when no specific error information is available

    console.error(`Error ${action}:`, error);
    throw new Error(`An error occurred while ${action}.`);
  }
};
