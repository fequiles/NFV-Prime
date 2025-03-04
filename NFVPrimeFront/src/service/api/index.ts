import { BaseService } from "@/service/base";
import { Store, StoreKey } from "../utils/store";
import { AuthService } from "../auth";

export interface IQueries {
  [key: string]: string | number | boolean | any[] | undefined;
}
export interface Payload {
  path: string;
  body?: any;
  headers?: Headers;
  expires?: number;
  queries?: IQueries;
  signal?: AbortSignal;
  refreshToken?: boolean;
}
export interface BaseRequestInit extends RequestInit {
  queries?: IQueries;
}

export abstract class BaseApiService extends BaseService {
  protected readonly host: string;

  constructor(id: string, path?: string, host?: string) {
    super(id);
    this.host = [host ?? process.env.API_URL, path].join("/");
  }
  private isNullable(value: any) {
    return [undefined, null, ""].includes(value);
  }

  private clearJson(value: any): any {
    // clear recursive
    if (Array.isArray(value)) {
      if (value.filter((e) => !this.isNullable(e)).length === 0) {
        return undefined;
      }
      return value.map((e) => this.clearJson(e));
    }
    if (this.isNullable(value) || Number.isNaN(value)) {
      return undefined;
    }
    if (typeof value === "object") {
      Object.keys(value).forEach((k) => {
        value[k] = this.clearJson(value[k]);
      });

      if (
        Object.keys(value).length === 0 ||
        !Object.values(value).some((e) => !this.isNullable(e))
      ) {
        return undefined;
      }
    }

    return value;
  }

  protected getUrl(path: string, options: BaseRequestInit) {
    let url = `${this.host}/${path}`;

    if (options.queries) {
      const keys = Object.keys(options.queries).sort();
      if (keys.length) {
        const q = keys
          .map((k) => {
            if (!options.queries || !options.queries[k]) {
              return undefined;
            }
            if (Array.isArray(options.queries[k])) {
              return `${k}=${encodeURIComponent(
                (options.queries[k] as any[]).join(",")
              )}`;
            }

            return `${k}=${encodeURIComponent(`${options.queries[k]}`)}`;
          })
          .filter((e) => e)
          .join("&");

        if (q.length) {
          url += `?${q}`;
        }
      }
    }

    return url;
  }

  protected async requestByPath(
    path: string,
    options: BaseRequestInit,
    refreshToken?: boolean
  ) {
    const url = this.getUrl(path, options);

    return this.request(url, options, refreshToken);
  }

  protected async request(
    url: string,
    options: RequestInit,
    refreshToken?: boolean
  ) {
    if (!options.headers) {
      options.headers = new Headers({});
    }

    if (AuthService.tokenExpired && !refreshToken) {
      await AuthService.refreshToken();
    }

    const token = Store.getItem(StoreKey.AUTH_TOKEN);

    if (token && !refreshToken) {
      (options.headers as Headers).append("Authorization", `Bearer ${token}`);
    }

    if (refreshToken) {
      const tokenRef = Store.getItem(StoreKey.REFRESH_TOKEN);

      (options.headers as Headers).append(
        "Authorization",
        `Bearer ${tokenRef}` ?? ""
      );
    }

    if (options.body) {
      (options.headers as Headers).append("Content-Type", "application/json");
    }
    // TODO: force work with next
    if (typeof window === "undefined") {
      (options.headers as Headers).append("Origin", `http://localhost:3001`);
    }

    let res: any;
    try {
      res = await fetch(url, options);
    } catch (err) {
      // eslint-disable-next-line no-throw-literal
      throw {
        code: "API_CRASH",
        message: "Ops! Try again later.",
      };
    }

    switch (res.status) {
      case 0:
        throw {
          code: "API_OFFLINE",
          message: "Ops! Looks like offline.",
        };
      case 204: // no content
      case 404:
        return undefined;
      case 401:
        if (res.statusText === "Unauthorized") {
          throw {
            code: "AUTH_FAIL",
            message: "Ops! Invalid email or password.",
          };
        }
      default:
        break;
    }

    if (res.status < 200 || res.status > 299) {
      const { err, message } = await res.json();
      console.error("API", {
        status: res.status,
        err,
        message,
      });
      if (err) {
        const errValue = Array.isArray(err) ? err[0] : err;
        throw errValue;
      }

      // eslint-disable-next-line no-throw-literal
      throw {
        code: "NOT_DEFINED",
        message: "Ops! Something gone wrong.",
      };
    }

    return await res.json();
  }
  async get({ path, headers, queries, expires, signal }: Payload) {
    const res = await this.requestByPath(path, {
      method: "GET",
      headers,
      queries: {
        ...queries,
        expires,
      },
      signal,
    });
    return res;
  }
  async delete({ path, headers, queries, body, signal }: Payload) {
    const res = await this.requestByPath(path, {
      method: "DELETE",
      body: body ? JSON.stringify(this.clearJson(body)) : undefined,
      headers,
      queries,
      signal,
    });
    return res;
  }
  async post({ path, headers, queries, body, signal, refreshToken }: Payload) {
    const res = await this.requestByPath(
      path,
      {
        method: "POST",
        body: body ? JSON.stringify(this.clearJson(body)) : undefined,
        headers,
        queries,
        signal,
      },
      refreshToken
    );
    return res;
  }
  async put({ path, headers, queries, body, signal }: Payload) {
    const res = await this.requestByPath(path, {
      method: "PUT",
      body: body ? JSON.stringify(this.clearJson(body)) : undefined,
      headers,
      queries,
    });
    return res;
  }
  async patch({ path, headers, queries, body, signal }: Payload) {
    const res = await this.requestByPath(path, {
      method: "PATCH",
      body: body ? JSON.stringify(this.clearJson(body)) : undefined,
      headers,
      queries,
      signal,
    });
    return res;
  }
}
