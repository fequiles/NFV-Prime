import { InboxOutlined } from '@ant-design/icons';
import type { UploadFile, UploadProps } from 'antd';
import { message, Upload as UploadAntd } from 'antd';

const { Dragger } = UploadAntd;

const props: UploadProps = {
  name: 'file',
  multiple: true,
  action: 'https://run.mocky.io/v3/435e224c-44fb-4773-9faf-380c5e6a2188',
  // onChange(info) {
  //   const { status } = info.file as UploadFile;
  //   if (status !== 'uploading') {
  //     console.log(info.file, info.fileList);
  //     let reader = new FileReader();
  //       reader.onload = (e) => {
  //          console.log(e.target.result);
  //       }
  //       reader.readAsText(info.file.originFileObj);

  //   }
  //   if (status === 'done') {
  //     message.success(`${info.file.name} file uploaded successfully.`);
  //   } else if (status === 'error') {
  //     message.error(`${info.file.name} file upload failed.`);
  //   }
  // },
  onChange(info) {
    if (!info) return

    if (info.file.status !== 'uploading') {
       let reader = new FileReader();
        reader.onload = (e: any) => {
          if (!e) return

           console.log(e.target.result);
        }
        reader.readAsText(info.file.originFileObj as any);
    }
    if (info.file.status === 'done') {
      message.success(`${info.file.name} file uploaded successfully`);
    } else if (info.file.status === 'error') {
      message.error(`${info.file.name} file upload failed.`);
    }
  },
  onDrop(e) {
    console.log('Dropped files', e.dataTransfer.files);
  },
  
};

export default function Upload() { 
  return(
    <Dragger {...props}>
        <p className="ant-upload-drag-icon">
        <InboxOutlined />
        </p>
        <p className="ant-upload-text">Clique ou arraste anexar um arquivo</p>
        <p className="ant-upload-hint">
        Clique ou arraste aqui 
        </p>
    </Dragger>
)};

