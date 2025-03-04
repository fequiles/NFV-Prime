import { ITraffic } from "../traffic/interface";

export interface IListInterface {
  id: number;
  name: string;
  host: string;
}

export interface IExportedJson {
  code: string;
  interfacesNumber: number;
  traffics: ITraffic[]
}