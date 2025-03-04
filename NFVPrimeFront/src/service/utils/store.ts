enum StoreKey {
  AUTH_TOKEN = "auth:token",
  LOGIN_UID = "login:uid",
  HOLDING_UID = "holding:uid",
  REFRESH_TOKEN = "refresh:token",
}

class Store {
  private cache: { [key: string]: string };
  constructor() {
    this.cache = {};
  }
  getItem(id: StoreKey | string) {
    if (typeof window === "undefined") {
      return this.cache[id];
    }
    const res = localStorage.getItem(id);
    if (!res) {
      return undefined;
    }
    return res;
  }
  setItem(id: StoreKey | string, value: string) {
    if (typeof window === "undefined") {
      this.cache[id] = value;
      return;
    }
    localStorage.setItem(id, value);
  }
  removeItem(id: StoreKey | string) {
    if (typeof window === "undefined") {
      delete this.cache[id];
      return;
    }
    localStorage.removeItem(id);
  }
}

const Service = new Store();

export { Service as Store, StoreKey };
