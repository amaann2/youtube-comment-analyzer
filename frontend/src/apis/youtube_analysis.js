import { API_BASE_URL } from "../config";
import axios from "axios";
import { handleErrors } from "../utils/apiErrorHandler";

export const analyzeComments = async (requestBody) => {
  try {
    const response = await axios.post(
      `${API_BASE_URL}/api/analysis`,
      requestBody
    );

    if (response.status !== 200) {
      throw new Error(response.data.detail || "An error occurred");
    }

    return await response.data;
  } catch (error) {
    handleErrors(error, "analyzeComments");
  }
};

export const getAnalysisData = async (id) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/media/${id}/data.json`);
    return await response.data;
  } catch (error) {
    handleErrors(error, "getAnalysisData");
  }
};
