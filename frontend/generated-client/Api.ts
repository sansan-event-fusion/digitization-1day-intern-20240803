/* eslint-disable */
/* tslint:disable */
/*
 * ---------------------------------------------------------------
 * ## THIS FILE WAS GENERATED VIA SWAGGER-TYPESCRIPT-API        ##
 * ##                                                           ##
 * ## AUTHOR: acacode                                           ##
 * ## SOURCE: https://github.com/acacode/swagger-typescript-api ##
 * ---------------------------------------------------------------
 */

/** EntryItems */
export type ApiEntryItems = "full_name" | "email" | "company_name" | "position_name" | "address";

/** EntryModel */
export interface ApiEntryModel {
  /**
   * Full Name
   * 名前
   */
  full_name: string;
  /**
   * Email
   * メールアドレス
   */
  email: string;
  /**
   * Company Name
   * 会社名
   */
  company_name: string;
  /**
   * Position Name
   * 部署名
   */
  position_name: string;
  /**
   * Address
   * 住所
   */
  address: string;
}

/** HTTPValidationError */
export interface ApiHTTPValidationError {
  /** Detail */
  detail?: ApiValidationError[];
}

/** InspectedVirtualCardModel */
export interface ApiInspectedVirtualCardModel {
  /**
   * Inspected Items
   * 修正が必要な項目名のリスト
   * @default []
   */
  inspected_items?: ApiEntryItems[];
  /**
   * Id
   * 名刺のID
   */
  id: string;
  /**
   * Image Path
   * 名刺の画像のパス
   */
  image_path: string | null;
  /** 名刺のデータ化項目 */
  entry: ApiEntryModel;
  /**
   * Created At
   * 作成日時
   */
  created_at: string;
  /**
   * Delivered At
   * 納品日時
   */
  delivered_at?: string | null;
}

/**
 * InspectionResult
 * 検証の結果を格納するモデル
 * `inspected_items` で修正が必要な項目名のリストを指定する。
 *
 * fields:
 *     inspected_items: List[EntryItems]: 修正が必要な項目名のリスト
 */
export interface ApiInspectionResult {
  /**
   * Inspected Items
   * 修正が必要な項目名のリスト
   * @default []
   */
  inspected_items?: ApiEntryItems[];
}

/** ValidationError */
export interface ApiValidationError {
  /** Location */
  loc: (string | number)[];
  /** Message */
  msg: string;
  /** Error Type */
  type: string;
}

/** VirtualCard */
export interface ApiVirtualCard {
  /** Image Path */
  image_path: string | null;
  entry: ApiEntryModel;
  /**
   * Id
   * @default "cc7fddb0bfec4acd86f808bf9344fd5b"
   */
  id?: string;
  /**
   * Created At
   * @default "2024-07-16T11:35:53.269401"
   */
  created_at?: string;
  /** Delivered At */
  delivered_at?: string | null;
}

/** VirtualCardCreate */
export interface ApiVirtualCardCreate {
  /** Image Path */
  image_path: string | null;
  entry: ApiEntryModel;
}

/** VirtualCardCreateBulk */
export interface ApiVirtualCardCreateBulk {
  /** Entries */
  entries: ApiVirtualCardCreate[];
}

/** VirtualCardModel */
export interface ApiVirtualCardModel {
  /**
   * Id
   * 名刺のID
   */
  id: string;
  /**
   * Image Path
   * 名刺の画像のパス
   */
  image_path: string | null;
  /** 名刺のデータ化項目 */
  entry: ApiEntryModel;
  /**
   * Created At
   * 作成日時
   */
  created_at: string;
  /**
   * Delivered At
   * 納品日時
   */
  delivered_at?: string | null;
}

export type QueryParamsType = Record<string | number, any>;
export type ResponseFormat = keyof Omit<Body, "body" | "bodyUsed">;

export interface FullRequestParams extends Omit<RequestInit, "body"> {
  /** set parameter to `true` for call `securityWorker` for this request */
  secure?: boolean;
  /** request path */
  path: string;
  /** content type of request body */
  type?: ContentType;
  /** query params */
  query?: QueryParamsType;
  /** format of response (i.e. response.json() -> format: "json") */
  format?: ResponseFormat;
  /** request body */
  body?: unknown;
  /** base url */
  baseUrl?: string;
  /** request cancellation token */
  cancelToken?: CancelToken;
}

export type RequestParams = Omit<FullRequestParams, "body" | "method" | "query" | "path">;

export interface ApiConfig<SecurityDataType = unknown> {
  baseUrl?: string;
  baseApiParams?: Omit<RequestParams, "baseUrl" | "cancelToken" | "signal">;
  securityWorker?: (securityData: SecurityDataType | null) => Promise<RequestParams | void> | RequestParams | void;
  customFetch?: typeof fetch;
}

export interface HttpResponse<D extends unknown, E extends unknown = unknown> extends Response {
  data: D;
  error: E;
}

type CancelToken = Symbol | string | number;

export enum ContentType {
  Json = "application/json",
  FormData = "multipart/form-data",
  UrlEncoded = "application/x-www-form-urlencoded",
  Text = "text/plain",
}

export class HttpClient<SecurityDataType = unknown> {
  public baseUrl: string = "";
  private securityData: SecurityDataType | null = null;
  private securityWorker?: ApiConfig<SecurityDataType>["securityWorker"];
  private abortControllers = new Map<CancelToken, AbortController>();
  private customFetch = (...fetchParams: Parameters<typeof fetch>) => fetch(...fetchParams);

  private baseApiParams: RequestParams = {
    credentials: "same-origin",
    headers: {},
    redirect: "follow",
    referrerPolicy: "no-referrer",
  };

  constructor(apiConfig: ApiConfig<SecurityDataType> = {}) {
    Object.assign(this, apiConfig);
  }

  public setSecurityData = (data: SecurityDataType | null) => {
    this.securityData = data;
  };

  protected encodeQueryParam(key: string, value: any) {
    const encodedKey = encodeURIComponent(key);
    return `${encodedKey}=${encodeURIComponent(typeof value === "number" ? value : `${value}`)}`;
  }

  protected addQueryParam(query: QueryParamsType, key: string) {
    return this.encodeQueryParam(key, query[key]);
  }

  protected addArrayQueryParam(query: QueryParamsType, key: string) {
    const value = query[key];
    return value.map((v: any) => this.encodeQueryParam(key, v)).join("&");
  }

  protected toQueryString(rawQuery?: QueryParamsType): string {
    const query = rawQuery || {};
    const keys = Object.keys(query).filter((key) => "undefined" !== typeof query[key]);
    return keys
      .map((key) => (Array.isArray(query[key]) ? this.addArrayQueryParam(query, key) : this.addQueryParam(query, key)))
      .join("&");
  }

  protected addQueryParams(rawQuery?: QueryParamsType): string {
    const queryString = this.toQueryString(rawQuery);
    return queryString ? `?${queryString}` : "";
  }

  private contentFormatters: Record<ContentType, (input: any) => any> = {
    [ContentType.Json]: (input: any) =>
      input !== null && (typeof input === "object" || typeof input === "string") ? JSON.stringify(input) : input,
    [ContentType.Text]: (input: any) => (input !== null && typeof input !== "string" ? JSON.stringify(input) : input),
    [ContentType.FormData]: (input: any) =>
      Object.keys(input || {}).reduce((formData, key) => {
        const property = input[key];
        formData.append(
          key,
          property instanceof Blob
            ? property
            : typeof property === "object" && property !== null
            ? JSON.stringify(property)
            : `${property}`,
        );
        return formData;
      }, new FormData()),
    [ContentType.UrlEncoded]: (input: any) => this.toQueryString(input),
  };

  protected mergeRequestParams(params1: RequestParams, params2?: RequestParams): RequestParams {
    return {
      ...this.baseApiParams,
      ...params1,
      ...(params2 || {}),
      headers: {
        ...(this.baseApiParams.headers || {}),
        ...(params1.headers || {}),
        ...((params2 && params2.headers) || {}),
      },
    };
  }

  protected createAbortSignal = (cancelToken: CancelToken): AbortSignal | undefined => {
    if (this.abortControllers.has(cancelToken)) {
      const abortController = this.abortControllers.get(cancelToken);
      if (abortController) {
        return abortController.signal;
      }
      return void 0;
    }

    const abortController = new AbortController();
    this.abortControllers.set(cancelToken, abortController);
    return abortController.signal;
  };

  public abortRequest = (cancelToken: CancelToken) => {
    const abortController = this.abortControllers.get(cancelToken);

    if (abortController) {
      abortController.abort();
      this.abortControllers.delete(cancelToken);
    }
  };

  public request = async <T = any, E = any>({
    body,
    secure,
    path,
    type,
    query,
    format,
    baseUrl,
    cancelToken,
    ...params
  }: FullRequestParams): Promise<HttpResponse<T, E>> => {
    const secureParams =
      ((typeof secure === "boolean" ? secure : this.baseApiParams.secure) &&
        this.securityWorker &&
        (await this.securityWorker(this.securityData))) ||
      {};
    const requestParams = this.mergeRequestParams(params, secureParams);
    const queryString = query && this.toQueryString(query);
    const payloadFormatter = this.contentFormatters[type || ContentType.Json];
    const responseFormat = format || requestParams.format;

    return this.customFetch(`${baseUrl || this.baseUrl || ""}${path}${queryString ? `?${queryString}` : ""}`, {
      ...requestParams,
      headers: {
        ...(requestParams.headers || {}),
        ...(type && type !== ContentType.FormData ? { "Content-Type": type } : {}),
      },
      signal: (cancelToken ? this.createAbortSignal(cancelToken) : requestParams.signal) || null,
      body: typeof body === "undefined" || body === null ? null : payloadFormatter(body),
    }).then(async (response) => {
      const r = response as HttpResponse<T, E>;
      r.data = null as unknown as T;
      r.error = null as unknown as E;

      const data = !responseFormat
        ? r
        : await response[responseFormat]()
            .then((data) => {
              if (r.ok) {
                r.data = data;
              } else {
                r.error = data;
              }
              return r;
            })
            .catch((e) => {
              r.error = e;
              return r;
            });

      if (cancelToken) {
        this.abortControllers.delete(cancelToken);
      }

      return data;
    });
  };
}

/**
 * @title FastAPI
 * @version 0.1.0
 */
export class Api<SecurityDataType extends unknown> extends HttpClient<SecurityDataType> {
  /**
   * No description
   *
   * @name ReadRootGet
   * @summary Read Root
   * @request GET:/
   */
  readRootGet = (params: RequestParams = {}) =>
    this.request<any, any>({
      path: `/`,
      method: "GET",
      format: "json",
      ...params,
    });

  card = {
    /**
     * @description 納品されたVirtualCardの一覧を返す
     *
     * @name ListDeliveredVirtualCards
     * @summary List Virtual Cards
     * @request GET:/card
     */
    listDeliveredVirtualCards: (params: RequestParams = {}) =>
      this.request<ApiVirtualCard[], any>({
        path: `/card`,
        method: "GET",
        format: "json",
        ...params,
      }),

    /**
     * @description 指定されたIDの納品済みVirtualCardを返す
     *
     * @name GetDeliveredVirtualCard
     * @summary Get Virtual Card
     * @request GET:/card/{card_id}
     */
    getDeliveredVirtualCard: (cardId: string, params: RequestParams = {}) =>
      this.request<ApiVirtualCard, ApiHTTPValidationError>({
        path: `/card/${cardId}`,
        method: "GET",
        format: "json",
        ...params,
      }),
  };
  virtualCard = {
    /**
     * @description 指定されたIDのデータを対象にノーマライズおよびインスペクターを実行する
     *
     * @name CreateVirtualCardTask
     * @summary Create Virtual Card Task
     * @request POST:/virtual_card/task/{card_id}
     */
    createVirtualCardTask: (cardId: string, params: RequestParams = {}) =>
      this.request<any, ApiHTTPValidationError>({
        path: `/virtual_card/task/${cardId}`,
        method: "POST",
        format: "json",
        ...params,
      }),

    /**
     * @description `/virtual_card`に格納されているデータを対象にノーマライズおよびインスペクターを実行する
     *
     * @name CreateVirtualCardTasks
     * @summary Create Virtual Card Tasks
     * @request POST:/virtual_card/tasks
     */
    createVirtualCardTasks: (params: RequestParams = {}) =>
      this.request<any, any>({
        path: `/virtual_card/tasks`,
        method: "POST",
        format: "json",
        ...params,
      }),

    /**
     * @description VirtualCardの一覧を返す
     *
     * @name ListVirtualCards
     * @summary List Virtual Cards
     * @request GET:/virtual_card
     */
    listVirtualCards: (params: RequestParams = {}) =>
      this.request<ApiVirtualCard[], any>({
        path: `/virtual_card`,
        method: "GET",
        format: "json",
        ...params,
      }),

    /**
     * @description 入力を受け取りVirtualCardを作成し、ノーマライズおよびインスペクターを実行する
     *
     * @name CreateVirtualCard
     * @summary Create Virtual Card
     * @request POST:/virtual_card
     */
    createVirtualCard: (data: ApiVirtualCardCreate, params: RequestParams = {}) =>
      this.request<any, ApiHTTPValidationError>({
        path: `/virtual_card`,
        method: "POST",
        body: data,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * @description 複数の入力を受け取りVirtualCardを作成し、ノーマライズおよびインスペクターを実行する
     *
     * @name CreateVirtualCards
     * @summary Create Virtual Cards
     * @request POST:/virtual_card/bulk
     */
    createVirtualCards: (data: ApiVirtualCardCreateBulk, params: RequestParams = {}) =>
      this.request<any, ApiHTTPValidationError>({
        path: `/virtual_card/bulk`,
        method: "POST",
        body: data,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * @description 指定されたIDのVirtualCardを返す
     *
     * @name GetVirtualCard
     * @summary Get Virtual Card
     * @request GET:/virtual_card/{card_id}
     */
    getVirtualCard: (cardId: string, params: RequestParams = {}) =>
      this.request<ApiVirtualCard, ApiHTTPValidationError>({
        path: `/virtual_card/${cardId}`,
        method: "GET",
        format: "json",
        ...params,
      }),
  };
  normalizer = {
    /**
     * @description ユーザーの入力をノーマライズする
     *
     * @name Normalize
     * @summary Normalizer
     * @request POST:/normalizer
     */
    normalize: (data: ApiEntryModel, params: RequestParams = {}) =>
      this.request<ApiEntryModel, ApiHTTPValidationError>({
        path: `/normalizer`,
        method: "POST",
        body: data,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),
  };
  inspector = {
    /**
     * @description 定義されたルールに従ってVirtualCardを検証する
     *
     * @name Inspect
     * @summary Inspect
     * @request POST:/inspector
     */
    inspect: (data: ApiVirtualCardModel, params: RequestParams = {}) =>
      this.request<ApiInspectionResult, ApiHTTPValidationError>({
        path: `/inspector`,
        method: "POST",
        body: data,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * @description インスペクター入力対象のVirtualCardをランダムに1件返す
     *
     * @name NewInspectorEntry
     * @summary New Inspector Entry
     * @request GET:/inspector/new
     */
    newInspectorEntry: (params: RequestParams = {}) =>
      this.request<ApiInspectedVirtualCardModel, any>({
        path: `/inspector/new`,
        method: "GET",
        format: "json",
        ...params,
      }),

    /**
     * @description ユーザーの入力を受け取りインスペクター入力の1入力を作成する
     *
     * @name CreateInspectorEntry
     * @summary Create Inspector Entry
     * @request POST:/inspector/create
     */
    createInspectorEntry: (data: ApiVirtualCardModel, params: RequestParams = {}) =>
      this.request<any, ApiHTTPValidationError>({
        path: `/inspector/create`,
        method: "POST",
        body: data,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),
  };
}
