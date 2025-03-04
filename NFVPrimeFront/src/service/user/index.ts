import { BaseApiService } from "../api";
import { IUser } from "./interface";

class UserService extends BaseApiService {
  constructor() {
    super("UserService", "user");
  }

  async get(): Promise<IUser[]> {
    const res = await super.get({
      path: ``,
    });

    return res;
  }
}

const service = new UserService();

export { service as UserService };
