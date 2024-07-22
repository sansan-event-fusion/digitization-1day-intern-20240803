import { ApiHTTPValidationError, ApiVirtualCard } from "@/generated-client/Api";
import { Result, apiClient, extractData } from "./client";

export const fetchDeliveredVirtualCards = async (): Promise<
  Result<ApiVirtualCard[], ApiHTTPValidationError>
> => {
  try {
    const client = apiClient();
    const response = await client.card.listDeliveredVirtualCards();

    return extractData<ApiVirtualCard[], ApiHTTPValidationError>(response);
  } catch (e) {
    return {
      success: false,
      data: { detail: [{ loc: [], msg: "unknown", type: "unknown" }] },
    };
  }
};
