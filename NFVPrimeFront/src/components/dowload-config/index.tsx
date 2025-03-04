import { DownloadOutlined } from "@ant-design/icons";
import { Button } from "antd";

interface IProps {
  data: Record<string, any>;
  filename: string;
  started: boolean
}

export default function ConfigDownload({ data, filename, started }: IProps) {
  const downloadJsonFile = () => {
    const json = JSON.stringify(data, null, 2); // transforma o objeto em string formatada
    const blob = new Blob([json], { type: "application/json" });
    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = url;
    link.download = `${filename}.json`;
    link.click();

    // Limpa o URL Blob após o download
    URL.revokeObjectURL(url);
  };

  return (
    <Button
      icon={<DownloadOutlined />}
      disabled={started}
      onClick={() => downloadJsonFile()}
    >
      Export
    </Button>
  );
}
