"use client";

import "./style.css";
import { Button, Form } from "antd";
import { useState } from "react";
import Card from "@/components/card";
import { notifyError } from "@/components/notification";
import InterfaceList from "./list";
import { TrafficService } from "@/service/traffic";
import { IListInterface } from "@/service/interfaces/interface";
import { InterfaceService } from "@/service/interfaces";
import { IExportedJson } from "@/service/nfvprime/interface";

interface IProps {
  interfacesList : IListInterface[];
  setInterfacesList : (list: IListInterface[]) => void;
  exportedJson: IExportedJson;
  setExportedJson: (obj: IExportedJson) => void;
}

export default function Interface({interfacesList, setInterfacesList, exportedJson, setExportedJson}: IProps) {
  const [submitting, setSubmitting] = useState(false);

  async function onSubmit() {
    setSubmitting(true);

    try {
      // call service
      const interfaces : IListInterface[] = []
      const res = await InterfaceService.start()
      Object.values(res).forEach((e: any) => interfaces.push(e))
      setInterfacesList(interfaces.sort())
      let newExported = {...exportedJson}
      newExported.interfacesNumber = interfaces.length - 1
      setExportedJson(newExported)
    } catch (err: any) {
      notifyError({ content: err?.message });
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div>
      <div className="card-interface">
        <Card>
          <div className="header-inteface-card">
            <span>Interfaces</span>
            <Button type="default" id="btn-start" onClick={onSubmit} loading={submitting}>
              New Interface
            </Button>
          </div>
          <InterfaceList
            interfacesList={interfacesList}
            setListInterfaces={setInterfacesList}
            exportedJson={exportedJson}
            setExportedJson={setExportedJson}
          />
        </Card>
      </div>
    </div>
  );
}
