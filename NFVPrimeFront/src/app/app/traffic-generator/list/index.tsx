import { DeleteOutlined, EditOutlined, PauseCircleOutlined, PlayCircleOutlined } from "@ant-design/icons";
import "./style.css";
import { Button, FormInstance, List } from "antd";
import { useState } from "react";
import { IListTraffic, ITraffic } from "@/service/traffic/interface";
import { TrafficService } from "@/service/traffic";
import { notifyError } from "@/components/notification";
import { IExportedJson } from "@/service/nfvprime/interface";

interface IProps {
  listTraffic: ITraffic[];
  setListTraffic: (list: ITraffic[]) => void;
  form: FormInstance,
  setType: (stype: string) => void,
  setManualTrafficGenerator: (stype: string) => void,
  exportedJson: IExportedJson;
  setExportedJson: (obj: IExportedJson) => void;
}

export default function InterfaceTraffic({ listTraffic, setListTraffic, form, setType, setManualTrafficGenerator, exportedJson, setExportedJson }: IProps) {

  const handleDeleteTraffic = async (item: ITraffic) => {
    try {
      let index = listTraffic.findIndex(elem => elem == item)
      const copy = [...listTraffic]
      copy.splice(index, 1)
      setListTraffic(copy)
    } catch (err: any){
      notifyError({content: err.message})
    }
  }

  const handleEditTraffic = async (item: ITraffic) => {
    if (item.type == 'Automatic') {
      setType(item.type)
      try {
        let index = listTraffic.findIndex(elem => elem == item)
        const copy = [...listTraffic]
        const removed = copy.splice(index, 1)
        const values = removed[0]
        form.setFieldsValue({
          name: values.name,
          rate: values.rate,
          lenght: values.lenght,
          count: values.count,
          delay: values.delay,
          port: values.port,
          trigger: values.trigger
        })
        // const res = await TrafficService.stop(item.pid.toString()) as IListTraffic[]
        setListTraffic(copy)
        let newExported = {...exportedJson}
        newExported.traffics = copy
        setExportedJson(newExported)
      } catch (err: any){
        notifyError({content: err.message})
      }
    } else {
      try {
        let index = listTraffic.findIndex(elem => elem == item)
        const copy = [...listTraffic]
        const removed = copy.splice(index, 1)
        setType(item.type)
        setManualTrafficGenerator(item.code)
        setListTraffic(copy)
        let newExported = {...exportedJson}
        newExported.traffics = copy
        setExportedJson(newExported)
      } catch (err: any){
        notifyError({content: err.message})
      }
    }
  }

  return (
    <>
      <span>List of Traffics</span>
      <List
        className="demo-loadmore-list"
        itemLayout="horizontal"
        dataSource={listTraffic}
        renderItem={(item) => (
          <List.Item>
            <List.Item.Meta
              title={<b>{item.name}</b>}
              description={!item.code ? `Rate: ${item.rate}; Packet Size: ${item.lenght}; Count: ${item.count}; Delay: ${item.delay}; Port: ${item.port}; Interface: ${item.interface}; Trigger: ${item.trigger}` : ''}
            />
            {/* {(playingTraffic && !playingTraffic[item.pid])
              ? <Button className="btn-icons float-right" shape="circle" icon={<PlayCircleOutlined />} onClick={() => handlePlayingTraffic(item.pid)} />
              : <Button className="btn-icons float-right" shape="circle" icon={<PauseCircleOutlined />} onClick={() => handlePlayingTraffic(item.pid)}/>} */}
            <Button className="btn-icons float-right" shape="circle" icon={<EditOutlined />} onClick={() => handleEditTraffic(item)} />
            <Button className="btn-icons float-right" shape="circle" icon={<DeleteOutlined key="list-delete" className="list-delete"/>} onClick={() => handleDeleteTraffic(item)} />
          </List.Item>
        )}
      />
    </>
  );
}
