export interface ITraffic {
  type: string;
  name: string;
  lenght: number;
  rate: number;
  delay: number;
  port: number;
  count: number;
  interface: number;
  trigger: number;
  code: string;
}

export interface IListTraffic {
  pid: number;
  processName: string;
}