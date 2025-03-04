import { message } from "antd";

interface IProps {
  content: string;
}

export function notifySuccess({ content }: IProps) {
  message.open({
    type: "success",
    content,
  });
}

export function notifyError({ content }: IProps) {
  message.open({
    type: "error",
    content,
  });
}

export function notifyInfo({ content }: IProps) {
  message.open({
    type: "info",
    content,
  });
}

export function notifyWarn({ content }: IProps) {
  message.open({
    type: "warning",
    content,
  });
}
