import { Api, HttpResponse } from "@/generated-client/Api";

export type Result<T, E> =
  | {
      success: true;
      data: T;
    }
  | {
      success: false;
      data: E;
    };

export const extractData = async <T, E>(
  response: HttpResponse<T, E>,
): Promise<Result<T, E>> => {
  if (!response.ok) {
    return {
      success: false,
      data: response.error,
    };
  }

  return {
    success: true,
    data: response.data,
  };
};

let singletonClient: Api<unknown>;

type Headers = Record<string, string>;

export const apiClient = (): Api<unknown> => {
  if (singletonClient) return singletonClient;

  const host = process.env.BACKEND_SERVICE_URL;

  const headers: Headers = {
    Accept: "application/json",
    "Content-Type": "application/json",
    "X-Requested-With": "dummy",
  };

  const requestInit: RequestInit = {
    mode: "cors",
    headers,
    credentials: "include",
    cache: "no-cache",
  };

  singletonClient = new Api({
    baseUrl: `${host}`,
    baseApiParams: { ...requestInit, format: "json" },
  });

  return singletonClient;
};
