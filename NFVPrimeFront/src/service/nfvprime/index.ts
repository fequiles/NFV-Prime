import { BaseApiService } from "../api";
import { body } from "../utils/bodyRequest";

class NFVPrimeService extends BaseApiService {
  constructor() {
    super("IListInterface", "nfvprime");
  }

  async start() {
    const res = await super.post({path: "startGraficos", body});
    return res
  }

  async getTrafficInfos() {  
    const res = await super.post({path: `getTrafficInfos`, body});
    return res
  }

  async getProcessInfos() {  
    const res = await super.post({path: `getProcessInfos`, body});
    return res
  }

  async stopAll() {
    const res = await super.post({path: `stopAll`, body: {...body, typeList: '\'traffic\', \'traffic_p\', \'sniffer\', \'program\', \'graphics\', \'process_sniffer\''}});

    return Object.values(res)
  }

  async stopAllProcesses() {
    const res = await super.post({path: `stopAllProcesses`, body: {...body, typeList: '\'traffic\', \'traffic_p\', \'program\', \'process_sniffer\''}});

    return Object.values(res)
  }
}

const service = new NFVPrimeService();

export { service as NFVPrimeService };
