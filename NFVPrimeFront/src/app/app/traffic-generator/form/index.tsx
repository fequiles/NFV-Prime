import "./style.css";
import { Form, FormInstance, Input, InputNumber, Select } from "antd";
import { ITraffic } from "@/service/traffic/interface";
import { IListInterface } from "@/service/interfaces/interface";
import { useEffect, useState } from "react";

interface IProps {
  form: FormInstance;
  submitting: boolean;
  interfaceList: IListInterface[];
}

export default function FormTraffic({
  form,
  submitting,
  interfaceList,
}: IProps) {
  const [selectInterfaceList, setSelectInterfaceList] = useState([]);

  useEffect(() => {
    if (!interfaceList?.length) {
      return;
    }

    const newInterfacesList: any = [];
    interfaceList.forEach((e: IListInterface) => {
      if (e.id != 0) {
        newInterfacesList.push({ value: e.id, label: e.name });
      }
    });
    setSelectInterfaceList(newInterfacesList);
  }, [interfaceList]);

  return (
    <Form
      className="traffic-form-container"
      layout="inline"
      labelWrap
      form={form}
      initialValues={
        {
          name: "",
          rate: 0,
          count: 0,
          delay: 0,
          port: 8001,
          lenght: 0,
          trigger: 0,
        } as ITraffic
      }
      scrollToFirstError={{
        behavior: "smooth",
        block: "center",
        inline: "center",
      }}
    >
      <Form.Item
        label={"Nome:"}
        tooltip="Info a mais"
        name="name"
        rules={[
          { required: true, message: "Ops! Fill this field." },
          {
            type: "string",
            message: "Ops! Invalid field..",
          },
        ]}
      >
        <Input
          disabled={submitting}
          className="width-input"
          placeholder="Traffic Name"
        />
      </Form.Item>

      <Form.Item
        label={"Rate (1-1000 packets/s):"}
        tooltip="Info a mais"
        name="rate"
        rules={[
          { required: true, message: "Ops! Fill this field." },
          {
            type: "number",
            min: 0,
            max: 1000,
            message: "Ops! Invalid field..",
          },
        ]}
      >
        <InputNumber
          disabled={submitting}
          min={1}
          max={1000}
          decimalSeparator=","
          precision={0}
        />
      </Form.Item>

      <Form.Item
        label={"Packet Size (0-65400 bytes):"}
        tooltip="Info a mais"
        name="lenght"
        rules={[
          { required: true, message: "Ops! Fill this field." },
          {
            type: "number",
            min: 0,
            max: 65400,
            message: "Ops! Invalid field..",
          },
        ]}
      >
        <InputNumber
          disabled={submitting}
          min={1}
          max={65400}
          decimalSeparator=","
          precision={0}
        />
      </Form.Item>

      <Form.Item
        label={"Number of packets to send (0-1000):"}
        tooltip="Info a mais"
        name="count"
        rules={[
          { required: true, message: "Ops! Fill this field." },
          {
            type: "number",
            min: 0,
            max: 1000,
            message: "Ops! Invalid field..",
          },
        ]}
      >
        <InputNumber
          disabled={submitting}
          min={0}
          max={1000}
          decimalSeparator=","
          precision={0}
        />
      </Form.Item>

      <Form.Item
        label={"Delay (s):"}
        tooltip="Info a mais"
        name="delay"
        rules={[
          { required: true, message: "Ops! Fill this field." },
          {
            type: "number",
            min: 0,
            max: 99999999,
            message: "Ops! Invalid field..",
          },
        ]}
      >
        <InputNumber
          disabled={submitting}
          min={1}
          max={99999999}
          decimalSeparator=","
          precision={0}
        />
      </Form.Item>

      <Form.Item
        label={"Port (1024-49151):"}
        tooltip="Info a mais"
        name="port"
        rules={[
          { required: true, message: "Ops! Fill this field." },
          {
            type: "number",
            min: 1024,
            max: 49151,
            message: "Ops! Invalid field..",
          },
        ]}
      >
        <InputNumber
          disabled={submitting}
          min={1024}
          max={49151}
          decimalSeparator=","
          precision={0}
        />
      </Form.Item>
      <Form.Item
        label={"Interface:"}
        tooltip="Info a mais"
        name="interface"
        rules={[{ required: true, message: "Ops! Fill this field." }]}
      >
        <Select
          placeholder="Select interface"
          className="width-input"
          options={selectInterfaceList}
          disabled={submitting}
        />
      </Form.Item>

      <Form.Item
        label={"Trigger (ms):"}
        tooltip="Info a mais"
        name="trigger"
        rules={[
          { required: true, message: "Ops! Fill this field." },
          {
            type: "number",
            min: 0,
            max: 99999999,
            message: "Ops! Invalid field..",
          },
        ]}
      >
        <InputNumber
          disabled={submitting}
          min={0}
          max={99999999}
          decimalSeparator=","
          precision={0}
        />
      </Form.Item>
    </Form>
  );
}
