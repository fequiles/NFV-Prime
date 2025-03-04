import { BaseApiService } from "../api";
import { body } from "../utils/bodyRequest";
import { IListInterface } from "./interface";

class InterfaceService extends BaseApiService {
  constructor() {
    super("IListInterface", "interface");
  }

  async start() {
    const res = await super.post({path: "createInterface", body});
    return res
  }

  async stop(id: string) {  
    const res = await super.delete({path: `deleteInterface/${id}`, body});
    return res
  }

  async deleteAllUserInterfaces() {  
    const res = await super.post({path: `deleteAllUserInterfaces`, body});
    return res
  }

  async search() {  
    const res = await super.post({path: `searchInterfaces`, body});

    return Object.values(res)
  }

   
}

const service = new InterfaceService();

export { service as InterfaceService };
