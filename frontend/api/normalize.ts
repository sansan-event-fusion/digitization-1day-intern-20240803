import { ApiEntryModel, ApiHTTPValidationError } from "@/generated-client/Api";
import { apiClient, extractData } from "./client";

export const normalize = async (params: ApiEntryModel) => {
  try {
    const client = apiClient();
    const response = await client.normalizer.normalize(params);

    return extractData<ApiEntryModel, ApiHTTPValidationError>(response);
  } catch (e) {
    return {
      success: false,
      data: "unknown",
    };
  }
};
