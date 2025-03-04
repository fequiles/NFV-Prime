"use client";

import { Form } from "antd";
import Canvas from "./canvas";
import "./style.css";
import Card from "@/components/card";
import { useState } from "react";
import FormGraphic from "./form";
import { IListInterface } from "@/service/interfaces/interface";

interface IProps {
  interfacesList : IListInterface[];
}

export default function Graphic({interfacesList}: IProps) {
  const [submitting, setSubmitting] = useState(false);
  const [interfaceMode, setInterfaceMode] = useState(true);

  const [form] = Form.useForm();
  return (
    <div className="container-graphic">
      <div>
        <FormGraphic form={form} submitting={submitting} interfacesList={interfacesList} interfaceMode={interfaceMode} setInterfaceMode={setInterfaceMode} />
      </div>
      <Card className="code-graphic">
        <Canvas form={form} interfaceMode={interfaceMode}/>
      </Card>
    </div>
  );
}
