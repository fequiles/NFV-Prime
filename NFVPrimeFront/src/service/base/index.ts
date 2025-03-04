export abstract class BaseService {
  protected readonly id: string;
  constructor(id: string) {
    this.id = id;
  }
}
