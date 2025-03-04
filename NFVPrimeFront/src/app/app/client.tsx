"use client";

import "./style.css";
import CodeEditor from "./code-editor";
import TrafficGenerator from "./traffic-generator";
import { useCallback, useEffect, useRef, useState } from "react";
import LoadingPage from "@/components/loading";
import Graphic from "./graphic";
import Interface from "./interface";
import { Button, Collapse, CollapseProps, Form, Upload } from "antd";
import { IListInterface } from "@/service/interfaces/interface";
import { notifyError, notifyInfo } from "@/components/notification";
import { InterfaceService } from "@/service/interfaces";
import { NFVPrimeService } from "@/service/nfvprime";
import { IListTraffic, ITraffic } from "@/service/traffic/interface";
import { CodeEditorService } from "@/service/codeEditor";
import { TrafficService } from "@/service/traffic";
import Help from "./help";
import { Footer } from "antd/es/layout/layout";
import { DownloadOutlined, UploadOutlined } from "@ant-design/icons";
import ConfigDownload from "@/components/dowload-config";
import { IExportedJson } from "@/service/nfvprime/interface";

export default function AppClient() {
  const [loading, setLoading] = useState(true);
  const [interfacesList, setInterfacesList] = useState<IListInterface[]>([]);
  const [code, setCode] = useState<string>();
  const [listTraffic, setListTraffic] = useState<ITraffic[]>([])
  const [submitting, setSubmitting] = useState(false);
  const [started, setStarted] = useState(false);
  const [exportedJson, setExportedJson] = useState<IExportedJson>({
    code: '',
    interfacesNumber: 0,
    traffics: []
  });

  const load =  useCallback(async () => {
    try {
      let interfaces : IListInterface[] = await InterfaceService.search() as IListInterface[]
      // call service
      if (interfaces.length < 2) {
        if (interfacesList.length == 0) {
          await InterfaceService.start()
        }

        const res = await InterfaceService.start()
        interfaces = []
        Object.values(res).forEach((e: any) => interfaces.push(e))
        setInterfacesList(interfaces.sort())
        let newExported = {...exportedJson}
        newExported.interfacesNumber = interfaces.length - 1
        setExportedJson(newExported)
      }
    } catch (err: any) {
      notifyError({content: err.message})
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    window.addEventListener("beforeunload", (ev) => {
      NFVPrimeService.stopAll() 
    });

    load()

  }, []);

  if (loading) {
    return <LoadingPage />;
  }

  const items: CollapseProps['items'] = [
    {
      key: '1',
      label: 'Help',
      children: <Help />,
    },
    {
      key: '2',
      label: 'VNF Code Editor',
      children: <CodeEditor code={code} setCode={setCode} exportedJson={exportedJson} setExportedJson={setExportedJson}/>,
    },
    {
      key: '3',
      label: 'Virtual Network Interfaces Manager',
      children: <Interface interfacesList={interfacesList} setInterfacesList={setInterfacesList} exportedJson={exportedJson} setExportedJson={setExportedJson}/>,
    },
    {
      key: '4',
      label: 'Traffic Generator',
      children: <TrafficGenerator 
                  interfacesList={interfacesList}
                  listTraffic={listTraffic}
                  setListTraffic={setListTraffic}
                  submitting={submitting}
                  setSubmitting={setSubmitting}
                  started={started} 
                  exportedJson={exportedJson}
                  setExportedJson={setExportedJson}/>,
    },
    {
      key: '5',
      label: 'Visualization',
      children: <Graphic interfacesList={interfacesList} />
    },
  ];

  async function onStarded() {
    setStarted(true);
    try {
      if (code) {
        try {
          CodeEditorService.start(code)
        } catch (err: any) {
          notifyError({content: err?.message})
        }
      } else {
        notifyInfo({ content: "The function code can't be empty" })
      }
      if (listTraffic.length > 0) {
        listTraffic.forEach(traffic => {
          setTimeout(() => {
            TrafficService.start(traffic)
          }, traffic.trigger)
        })
      }  else {
        notifyInfo({ content: "The traffic list can't be empty" })
      }
    } catch (err: any) {
      notifyError({ content: err?.message });
    }
  }

  async function onStopped() {
    try {
      NFVPrimeService.stopAllProcesses() 
    } catch (err: any) {
      notifyError({ content: err?.message });
    } finally {
      setStarted(false);
    }
  }

  const handleChange = (info) => {
    // Prevent automatic upload
    if (info.file.status !== "uploading") {
      const file = info.file.originFileObj;
      if (file) {
        const reader = new FileReader();
        reader.readAsText(file);
        reader.onload = async() => {
            const text = String(reader.result);
            const importedJson = JSON.parse(text);
            console.log(importedJson.code)
            if (importedJson.interfacesNumber != null) {
              await InterfaceService.deleteAllUserInterfaces()
              setInterfacesList([])
              let newExported = {...exportedJson}
              newExported.interfacesNumber = 0
              setExportedJson(newExported)
              for (let i = 0; i < importedJson.interfacesNumber; i++) {
                try {
                  const interfaces : IListInterface[] = [];
                  const res = await InterfaceService.start();
                  Object.values(res).forEach((e: any) => interfaces.push(e));
                  setInterfacesList(interfaces.sort());
                  let newExported = {...exportedJson}
                  newExported.interfacesNumber = interfaces.length - 1
                  setExportedJson(newExported)
                } catch (err: any) {
                  notifyError({ content: err?.message });
                }
              }
            }
            if (importedJson.code){
              setCode(importedJson.code)
            }
            if (importedJson.traffics && importedJson.traffics.length > 0) {
              setListTraffic([])
              let listTraffic : ITraffic[] = []
              for (let traffic of importedJson.traffics) {
                let newTraffic: ITraffic = {
                  type: traffic.type,
                  name: traffic.name,
                  lenght: traffic.lenght,
                  rate: traffic.rate,
                  delay: traffic.delay,
                  port: traffic.port,
                  count: traffic.count,
                  interface: traffic.interface,
                  trigger: traffic.trigger,
                  code: traffic.code
                }
                listTraffic.push(newTraffic);
              }
              setListTraffic(listTraffic)
            }
          }
        };
      }
  }

  return (
      <div className="container-app">
        <Collapse items={items} defaultActiveKey={['1']} />
        <div className="actions">
          {
            !started
            ? <Button type="default" id="btn-start" onClick={onStarded}>
                Start
              </Button>
            : <Button id="btn-stop" type="text" onClick={onStopped}>
                Stop
              </Button>
          }
          <Upload
            showUploadList={false}
            accept=".txt,.json"
            onChange={handleChange}
          >
            <Button disabled={started} icon={<UploadOutlined />}>Import</Button>
          </Upload>
          <ConfigDownload data={exportedJson} filename="config" started={started}/>
        </div>
      </div>
      
  );
}
