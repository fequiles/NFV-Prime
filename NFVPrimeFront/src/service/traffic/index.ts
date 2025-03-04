import { BaseApiService } from "../api";
import { body } from "../utils/bodyRequest";
import { IListTraffic, ITraffic } from "./interface";

class TrafficService extends BaseApiService {
  constructor() {
    super("TrafficService", "traffic");
  }

  async start(trafficMode: ITraffic): Promise<IListTraffic[]> {
    const res = await super.post({path: "postTrafficMode", body: {...body,...trafficMode}}) as IListTraffic[];
    return Object.values(res)
  }

  async stop(id: string) {  
    const res = await super.delete({path: `stopTraffic/${id}`, body});
    return Object.values(res)
  }

  async search() {  
    const res = await super.post({path: `searchTrafficsProfiles`, body});
    return Object.values(res) ?? []
  }
}

const service = new TrafficService();

export { service as TrafficService };
