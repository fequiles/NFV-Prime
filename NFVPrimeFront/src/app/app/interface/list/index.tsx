import { DeleteOutlined } from "@ant-design/icons";
import "./style.css";
import { Button, List } from "antd";
import { IListInterface } from "@/service/interfaces/interface";
import { InterfaceService } from "@/service/interfaces";
import { notifyError } from "@/components/notification";
import { IExportedJson } from "@/service/nfvprime/interface";

interface IProps {
  interfacesList: IListInterface[];
  setListInterfaces: (list: IListInterface[]) => void;
  exportedJson: IExportedJson;
  setExportedJson: (obj: IExportedJson) => void;
}

export default function InterfaceList({ interfacesList, setListInterfaces, exportedJson, setExportedJson }: IProps) {
  const handleDeleteInterface = async (item: IListInterface) => {
    try {
      const interfaces : IListInterface[] = []
      const res = await InterfaceService.stop(item.id.toString())
      Object.values(res).forEach((e: any) => interfaces.push(e))
      setListInterfaces(interfaces.sort())
      let newExported = {...exportedJson}
      newExported.interfacesNumber = interfaces.length - 1
      setExportedJson(newExported)
    } catch (err: any){
      notifyError({content: err.message})
    }
  }

  return (
    <List
      className="demo-loadmore-list"
      itemLayout="horizontal"
      dataSource={interfacesList}
      renderItem={(item) => (
        <List.Item>
          <List.Item.Meta
            title={<b>{item.name}</b>}
            description={`Host_Name: ${item.hostname}, NetNamespace_name: ${item.nsname},Host_IP: ${item.hostip}, NetNamespace_IP: ${item.nsip}, Host_Ethernet: ${item.hether}, Netnamespace_Ethernet: ${item.nsether}`}
          />
          {item.id != 0 ? <Button className="btn-icons float-right" shape="circle" icon={<DeleteOutlined key="list-delete" className="list-delete"/>} onClick={() => handleDeleteInterface(item)} /> : <></>}
        </List.Item>
      )}
    />
  );
}
