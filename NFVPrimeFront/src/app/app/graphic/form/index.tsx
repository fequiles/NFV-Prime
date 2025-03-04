import { IListInterface } from "@/service/interfaces/interface";
import { Form, FormInstance, Select } from "antd";
import { useEffect, useState } from "react";

interface IProps {
  form: FormInstance;
  submitting: boolean;
  interfacesList: IListInterface[];
  interfaceMode: Boolean;
  setInterfaceMode: (bool: boolean) => void;
}

export default function FormGraphic({ form, submitting, interfacesList, interfaceMode, setInterfaceMode }: IProps) {
  const [selectInterfaceList, setSelectInterfaceList] = useState([])

  useEffect(() => {
    if (!interfacesList?.length) {
      return
    }

    const newInterfacesList: any = [] 
    interfacesList.forEach((e: IListInterface) => newInterfacesList.push({ value: e.id, label: e.name }))
    setSelectInterfaceList(newInterfacesList)
  }, [interfacesList])

  function typeChanged (evt: String) {
    if (evt == 'Interface') {
      setInterfaceMode(true)
    } else {
      setInterfaceMode(false)
    }
  }

  return (
    <Form
      className="traffic-form-container"
      layout="inline"
      labelWrap
      form={form}
      scrollToFirstError={{
        behavior: "smooth",
        block: "center",
        inline: "center",
      }}
      initialValues={
        {
          type: 'Interface',
        }
      }

    >
      <Form.Item
        label={"Type:"}
        name="type"
        rules={[
          { required: true, message: "Ops! Fill this field." }
        ]}
      >
        <Select placeholder="Select type" className="select-interface" options={[{title:'Interface', value:'Interface'},{title:'Function', value:'Function'}]} onChange={typeChanged} disabled={submitting} />
      </Form.Item>
      
      {interfaceMode ? <Form.Item
        label={"Interface:"}
        name="interface"
        rules={[
          { required: true, message: "Ops! Fill this field." }
        ]}
      >
        <Select placeholder="Select interface" className="select-interface" options={selectInterfaceList} disabled={submitting} />
      </Form.Item> : <></>}
    </Form>
  );
}
 