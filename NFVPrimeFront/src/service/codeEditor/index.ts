import { BaseApiService } from "../api";
import { body } from "../utils/bodyRequest";
import { ICode } from "./code";

class CodeEditorService extends BaseApiService {
  constructor() {
    super("ICode", "program");
  }

  async start(code: String) {
    const codeBody = {...body, code, processName: 'program'}
    const res = await super.post({path: "postProgram", body: codeBody});
    return res
  }

  async stop() {  
    const res = await super.post({path: `stopProgram`, body});
    return res
  }

  async getSamples() {  
    const res = await super.post({path: `getProgramsSamples`, body});
    return res
  }
   
}

const service = new CodeEditorService();

export { service as CodeEditorService };
