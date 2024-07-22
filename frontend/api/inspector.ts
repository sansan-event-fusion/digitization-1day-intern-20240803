import {
  ApiHTTPValidationError,
  ApiInspectionResult,
  ApiInspectedVirtualCardModel,
  ApiVirtualCardModel,
} from "@/generated-client/Api";
import { apiClient, extractData } from "./client";

export const inspect = async (data: ApiVirtualCardModel) => {
  try {
    const client = apiClient();
    const response = await client.inspector.inspect(data);

    return extractData<ApiInspectionResult, ApiHTTPValidationError>(response);
  } catch (e) {
    return {
      success: false,
      data: "unknown",
    };
  }
};

export const newInspectEntry = async () => {
  try {
    const client = apiClient();
    const response = await client.inspector.newInspectorEntry();

    return extractData<ApiInspectedVirtualCardModel, string>(response);
  } catch (e) {
    return {
      success: false,
      data: "unknown",
    };
  }
};

export const createInspectorEntry = async (params: ApiVirtualCardModel) => {
  try {
    const client = apiClient();
    const response = await client.inspector.createInspectorEntry(params);

    return extractData<undefined, ApiHTTPValidationError>(response);
  } catch (e) {
    return {
      success: false,
      data: "unknown",
    };
  }
};
