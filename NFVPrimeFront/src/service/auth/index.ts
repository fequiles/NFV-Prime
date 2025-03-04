import { BaseApiService } from "../api";
import { Store, StoreKey } from "../utils/store";
import { IJwt, ISignInRes } from "./interface";

class AuthService extends BaseApiService {
  constructor() {
    super("AuthService", "auth");
  }

  private get Token(): IJwt | undefined {
    const data = Store.getItem(StoreKey.AUTH_TOKEN);
    if (!data) {
      return undefined;
    }
    return this.parseJwt(data) as IJwt;
  }

  get Username(): string | undefined {
    const data = Store.getItem(StoreKey.LOGIN_UID);
    if (!data) {
      return undefined;
    }
    return data;
  }

  get Name(): string | undefined {
    const jwt = this.Token;
    if (!jwt || !jwt.exp || !jwt.name) {
      return undefined;
    }
    return jwt.name;
  }

  get userId(): string | undefined {
    const jwt = this.Token;
    if (!jwt || !jwt.exp || !jwt.id) {
      return undefined;
    }
    return jwt.id;
  }

  get IsAuthenticated(): boolean {
    const jwt = this.Token;
    const jwtRefresh = Store.getItem(StoreKey.REFRESH_TOKEN);
    const refresh = jwtRefresh ? this.parseJwt(jwtRefresh) : undefined;

    if (!jwt || !jwt.exp) {
      return false;
    }

    if (jwt.exp * 1000 < Date.now()) {
      this.refreshToken();
    }

    if (!refresh || refresh.exp * 1000 < Date.now()) {
      return false;
    }

    return true;
  }

  get tokenExpired(): boolean {
    const jwt = this.Token;

    if (jwt && jwt.exp * 1000 < Date.now()) {
      return true;
    }

    return false;
  }

  async refreshToken() {
    const token = Store.getItem(StoreKey.REFRESH_TOKEN);
    const { accessToken, refreshToken }: ISignInRes = await super.post({
      path: "refresh",
      body: { token },
      refreshToken: true,
    });

    Store.setItem(StoreKey.AUTH_TOKEN, accessToken);
    Store.setItem(StoreKey.REFRESH_TOKEN, refreshToken);
  }

  signIn(username: string) {
    Store.setItem(StoreKey.LOGIN_UID, username);
  }

  private parseJwt(token: string): IJwt | undefined {
    try {
      const base64Url = token.split(".")[1];
      const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
      const jsonPayload = decodeURIComponent(
        atob(base64)
          .split("")
          .map((c) => {
            return "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2);
          })
          .join("")
      );

      return JSON.parse(jsonPayload);
    } catch {
      return undefined;
    }
  }

  signOut() {
    Store.removeItem(StoreKey.LOGIN_UID);
  }
}

const service = new AuthService();

export { service as AuthService };
